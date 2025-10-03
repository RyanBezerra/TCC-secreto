<?php
/**
 * Verificação de sessão
 * Endpoint para verificar se a sessão do usuário ainda é válida
 */

require_once 'auth.php';

// Verificar se a sessão é válida
$isValid = $auth->validateSession();

if ($isValid) {
    $user = $auth->getCurrentUser();
    echo json_encode([
        'valid' => true,
        'user' => [
            'id' => $user['id'],
            'nome' => $user['nome'],
            'cargo' => $user['cargo']
        ]
    ]);
} else {
    echo json_encode([
        'valid' => false,
        'message' => 'Sessão inválida ou expirada'
    ]);
}
?>
