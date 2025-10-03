<?php
/**
 * Verificação de autenticação para páginas protegidas
 * Redireciona para login se não autenticado
 */

require_once 'auth.php';

// Verificar se o usuário está autenticado
if (!$auth->isAuthenticated()) {
    // Registrar tentativa de acesso não autorizado
    $auth->logActivity(null, 'acesso_negado', 'Tentativa de acesso a página protegida sem autenticação');
    
    // Redirecionar para login
    header('Location: pages/registro/login/login.html');
    exit;
}

// Se autenticado, permitir acesso
// Este arquivo é incluído via .htaccess, então não precisa fazer mais nada
?>
