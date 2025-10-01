<?php
// Limpar qualquer output anterior
if (ob_get_level()) {
    ob_clean();
}

session_start();
require_once $_SERVER['DOCUMENT_ROOT'] . '/configDB.php';

// Definir header para JSON
header('Content-Type: application/json');

// Verificar se o formulário foi enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email'] ?? '');
    $senha = $_POST['senha'] ?? '';
    
    // Validações
    $erros = [];
    
    if (empty($email)) {
        $erros[] = 'Email é obrigatório';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $erros[] = 'Email inválido';
    }
    
    if (empty($senha)) {
        $erros[] = 'Senha é obrigatória';
    }
    
    // Se não há erros, verificar credenciais
    if (empty($erros)) {
        try {
            // Buscar usuário pelo email
            $stmt = $pdo->prepare("
                SELECT u.id, u.nome, u.email, u.senha_hash, u.cargo, u.status, e.nome_empresa 
                FROM usuarios u 
                LEFT JOIN empresas e ON u.empresa_id = e.id 
                WHERE u.email = ?
            ");
            $stmt->execute([$email]);
            $usuario = $stmt->fetch();
            
            if ($usuario) {
                // Verificar se a conta está ativa
                if ($usuario['status'] !== 'ativo') {
                    echo json_encode([
                        'success' => false,
                        'message' => 'Sua conta está inativa. Entre em contato com o administrador.'
                    ]);
                    exit;
                } else {
                    // Verificar senha
                    if (password_verify($senha, $usuario['senha_hash'])) {
                        // Login bem-sucedido - criar sessão
                        $_SESSION['usuario_id'] = $usuario['id'];
                        $_SESSION['usuario_nome'] = $usuario['nome'];
                        $_SESSION['usuario_email'] = $usuario['email'];
                        $_SESSION['usuario_cargo'] = $usuario['cargo'];
                        $_SESSION['empresa_nome'] = $usuario['nome_empresa'];
                        $_SESSION['logado'] = true;
                        
                        // Login bem-sucedido - não há coluna ultimo_acesso na tabela
                        
                        echo json_encode([
                            'success' => true,
                            'message' => 'Login realizado com sucesso! Redirecionando...'
                        ]);
                        exit;
                    } else {
                        echo json_encode([
                            'success' => false,
                            'message' => 'Senha incorreta'
                        ]);
                        exit;
                    }
                }
            } else {
                echo json_encode([
                    'success' => false,
                    'message' => 'Email não encontrado'
                ]);
                exit;
            }
            
        } catch (PDOException $e) {
            echo json_encode([
                'success' => false,
                'message' => 'Erro ao verificar credenciais: ' . $e->getMessage()
            ]);
            exit;
        }
    } else {
        echo json_encode([
            'success' => false,
            'message' => implode('<br>', $erros)
        ]);
        exit;
    }
}

// Se já estiver logado, retornar JSON
if (isset($_SESSION['logado']) && $_SESSION['logado'] === true) {
    echo json_encode([
        'success' => true,
        'message' => 'Usuário já está logado'
    ]);
    exit;
}

// Se não for uma requisição POST, retornar erro
echo json_encode([
    'success' => false,
    'message' => 'Método não permitido'
]);
exit;
