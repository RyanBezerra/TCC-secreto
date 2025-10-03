<?php
/**
 * Sistema de Autenticação e Logs
 * Gerencia sessões de usuários e registra atividades na tabela log
 */

session_start();
require_once 'configDB.php';

class AuthManager {
    private $pdo;
    
    public function __construct($pdo) {
        $this->pdo = $pdo;
    }
    
    /**
     * Verifica se o usuário está autenticado
     */
    public function isAuthenticated() {
        return isset($_SESSION['logado']) && $_SESSION['logado'] === true && 
               isset($_SESSION['usuario_email']) && !empty($_SESSION['usuario_email']);
    }
    
    /**
     * Registra login do usuário na tabela log
     */
    public function logLogin($usuarioId, $empresaId, $ip, $navegador) {
        try {
            $stmt = $this->pdo->prepare("
                INSERT INTO log (id_servidor, id_usuario, sql_exec, nm_tipo, nm_status, nm_ip, nm_navegador, nm_palavras_chave, fl_lista_atividade)
                VALUES (1, ?, 'LOGIN', 'login', 'sucesso', ?, ?, 'login_usuario', 1)
            ");
            $stmt->execute([$usuarioId, $ip, $navegador]);
            
            // Atualizar sessão com informações de log
            $_SESSION['login_time'] = time();
            $_SESSION['last_activity'] = time();
            
            return true;
        } catch (PDOException $e) {
            error_log("Erro ao registrar login: " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Registra logout do usuário
     */
    public function logLogout($usuarioId, $ip, $navegador) {
        try {
            $stmt = $this->pdo->prepare("
                INSERT INTO log (id_servidor, id_usuario, sql_exec, nm_tipo, nm_status, nm_ip, nm_navegador, nm_palavras_chave, fl_lista_atividade)
                VALUES (1, ?, 'LOGOUT', 'logout', 'sucesso', ?, ?, 'logout_usuario', 1)
            ");
            $stmt->execute([$usuarioId, $ip, $navegador]);
            return true;
        } catch (PDOException $e) {
            error_log("Erro ao registrar logout: " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Registra atividade do usuário
     */
    public function logActivity($usuarioId, $tipo, $descricao, $ip = null, $navegador = null) {
        try {
            $ip = $ip ?: $this->getClientIP();
            $navegador = $navegador ?: $this->getUserAgent();
            
            $stmt = $this->pdo->prepare("
                INSERT INTO log (id_servidor, id_usuario, sql_exec, nm_tipo, nm_status, nm_ip, nm_navegador, nm_palavras_chave, fl_lista_atividade)
                VALUES (1, ?, ?, ?, 'sucesso', ?, ?, ?, 1)
            ");
            $stmt->execute([$usuarioId, $descricao, $tipo, $ip, $navegador, $tipo . '_atividade']);
            return true;
        } catch (PDOException $e) {
            error_log("Erro ao registrar atividade: " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Verifica se a sessão ainda é válida
     */
    public function validateSession() {
        if (!$this->isAuthenticated()) {
            return false;
        }
        
        // Verificar timeout da sessão (2 horas)
        $sessionTimeout = 7200; // 2 horas em segundos
        if (isset($_SESSION['last_activity']) && 
            (time() - $_SESSION['last_activity']) > $sessionTimeout) {
            $this->logout();
            return false;
        }
        
        // Atualizar última atividade
        $_SESSION['last_activity'] = time();
        
        // Verificar se o usuário ainda existe e está ativo
        try {
            $stmt = $this->pdo->prepare("
                SELECT id, status FROM usuarios WHERE id = ?
            ");
            $stmt->execute([$_SESSION['usuario_id']]);
            $usuario = $stmt->fetch();
            
            if (!$usuario || $usuario['status'] !== 'ativo') {
                $this->logout();
                return false;
            }
            
            return true;
        } catch (PDOException $e) {
            error_log("Erro ao validar sessão: " . $e->getMessage());
            $this->logout();
            return false;
        }
    }
    
    /**
     * Força logout do usuário
     */
    public function logout() {
        if (isset($_SESSION['usuario_id'])) {
            // Registrar logout
            $this->logLogout($_SESSION['usuario_id'], $this->getClientIP(), $this->getUserAgent());
        }
        
        // Limpar todas as variáveis de sessão
        $_SESSION = array();
        
        // Destruir cookie de sessão
        if (ini_get("session.use_cookies")) {
            $params = session_get_cookie_params();
            setcookie(session_name(), '', time() - 42000,
                $params["path"], $params["domain"],
                $params["secure"], $params["httponly"]
            );
        }
        
        // Destruir sessão
        session_destroy();
    }
    
    /**
     * Redireciona para login se não autenticado
     */
    public function requireAuth($redirectTo = '/pages/registro/login/login.html') {
        if (!$this->validateSession()) {
            // Registrar tentativa de acesso não autorizado
            $this->logActivity(null, 'acesso_negado', 'Tentativa de acesso sem autenticação', $this->getClientIP(), $this->getUserAgent());
            
            header('Location: ' . $redirectTo);
            exit;
        }
    }
    
    /**
     * Obtém IP do cliente
     */
    private function getClientIP() {
        $ipKeys = ['HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'REMOTE_ADDR'];
        foreach ($ipKeys as $key) {
            if (array_key_exists($key, $_SERVER) === true) {
                foreach (explode(',', $_SERVER[$key]) as $ip) {
                    $ip = trim($ip);
                    if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE) !== false) {
                        return $ip;
                    }
                }
            }
        }
        return $_SERVER['REMOTE_ADDR'] ?? 'unknown';
    }
    
    /**
     * Obtém informações do navegador
     */
    private function getUserAgent() {
        return substr($_SERVER['HTTP_USER_AGENT'] ?? 'unknown', 0, 100);
    }
    
    /**
     * Obtém informações do usuário logado
     */
    public function getCurrentUser() {
        if (!$this->isAuthenticated()) {
            return null;
        }
        
        return [
            'id' => $_SESSION['usuario_id'],
            'nome' => $_SESSION['usuario_nome'],
            'email' => $_SESSION['usuario_email'],
            'cargo' => $_SESSION['usuario_cargo'],
            'empresa_nome' => $_SESSION['empresa_nome']
        ];
    }
}

// Instância global do gerenciador de autenticação
$auth = new AuthManager($pdo);
?>
