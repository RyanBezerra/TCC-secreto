<?php
/**
 * Logout do usuário
 * Registra o logout na tabela log e limpa a sessão
 */

require_once 'auth.php';

// Verificar se o usuário está logado
if ($auth->isAuthenticated()) {
    $user = $auth->getCurrentUser();
    
    // Registrar logout na tabela log
    $auth->logActivity($user['id'], 'logout', 'Logout do sistema');
    
    // Fazer logout
    $auth->logout();
    
    echo json_encode([
        'success' => true,
        'message' => 'Logout realizado com sucesso'
    ]);
} else {
    echo json_encode([
        'success' => false,
        'message' => 'Usuário não está logado'
    ]);
}
?>
