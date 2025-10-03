<?php
/**
 * Redirecionamento para dashboard com verificação de autenticação
 * Este arquivo substitui o acesso direto ao dashboard.html
 */

require_once 'auth.php';

// Verificar autenticação
if ($auth->isAuthenticated()) {
    // Se autenticado, redirecionar para o dashboard PHP
    header('Location: pages/dashboard/dashboard.php');
    exit;
} else {
    // Se não autenticado, redirecionar para login
    header('Location: pages/registro/login/login.html');
    exit;
}
?>
