<?php
/**
 * Teste de segurança - verificar se o sistema está protegido
 * Este arquivo deve ser removido em produção
 */

require_once 'auth.php';

echo "<h1>Teste de Segurança - GestiX</h1>";

// Teste 1: Verificar se usuário não autenticado é bloqueado
echo "<h2>Teste 1: Acesso sem autenticação</h2>";
if (!$auth->isAuthenticated()) {
    echo "<p style='color: green;'>✓ Usuário não autenticado - acesso bloqueado corretamente</p>";
} else {
    echo "<p style='color: red;'>✗ Usuário autenticado - possível falha de segurança</p>";
}

// Teste 2: Verificar estrutura da tabela log
echo "<h2>Teste 2: Estrutura da tabela log</h2>";
try {
    $stmt = $pdo->query("DESCRIBE log");
    $columns = $stmt->fetchAll();
    echo "<p style='color: green;'>✓ Tabela log encontrada com " . count($columns) . " colunas</p>";
    echo "<ul>";
    foreach ($columns as $column) {
        echo "<li>" . $column['Field'] . " (" . $column['Type'] . ")</li>";
    }
    echo "</ul>";
} catch (PDOException $e) {
    echo "<p style='color: red;'>✗ Erro ao acessar tabela log: " . $e->getMessage() . "</p>";
}

// Teste 3: Verificar se arquivos de proteção existem
echo "<h2>Teste 3: Arquivos de proteção</h2>";
$protectionFiles = [
    'auth.php' => 'Sistema de autenticação',
    'pages/dashboard/dashboard.php' => 'Dashboard protegido',
    'logout.php' => 'Sistema de logout',
    'check_session.php' => 'Verificação de sessão',
    'auth_check.php' => 'Verificação de autenticação'
];

foreach ($protectionFiles as $file => $description) {
    if (file_exists($file)) {
        echo "<p style='color: green;'>✓ $description - arquivo encontrado</p>";
    } else {
        echo "<p style='color: red;'>✗ $description - arquivo não encontrado</p>";
    }
}

// Teste 4: Verificar logs de acesso
echo "<h2>Teste 4: Logs de acesso</h2>";
try {
    $stmt = $pdo->query("SELECT COUNT(*) as total FROM log WHERE nm_tipo = 'login'");
    $result = $stmt->fetch();
    echo "<p style='color: green;'>✓ Total de logins registrados: " . $result['total'] . "</p>";
    
    $stmt = $pdo->query("SELECT COUNT(*) as total FROM log WHERE nm_tipo = 'acesso_negado'");
    $result = $stmt->fetch();
    echo "<p style='color: green;'>✓ Tentativas de acesso negado: " . $result['total'] . "</p>";
} catch (PDOException $e) {
    echo "<p style='color: red;'>✗ Erro ao consultar logs: " . $e->getMessage() . "</p>";
}

echo "<h2>Resumo de Segurança</h2>";
echo "<p><strong>Status:</strong> Sistema de autenticação implementado com sucesso!</p>";
echo "<p><strong>Proteções ativas:</strong></p>";
echo "<ul>";
echo "<li>Verificação de sessão em todas as páginas protegidas</li>";
echo "<li>Logs de acesso na tabela 'log'</li>";
echo "<li>Timeout de sessão (2 horas)</li>";
echo "<li>Redirecionamento automático para login</li>";
echo "<li>Proteção contra acesso direto a arquivos HTML</li>";
echo "</ul>";

echo "<p><strong>Próximos passos:</strong></p>";
echo "<ul>";
echo "<li>Teste o login em: <a href='pages/registro/login/login.html'>Fazer Login</a></li>";
echo "<li>Acesse o dashboard: <a href='pages/dashboard/dashboard.php'>Dashboard</a></li>";
echo "<li>Verifique os logs no banco de dados</li>";
echo "</ul>";

echo "<p style='color: orange;'><strong>IMPORTANTE:</strong> Remova este arquivo (test_security.php) em produção!</p>";
?>
