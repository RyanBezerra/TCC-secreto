<?php
$dbHost = 'localhost'; // banco no mesmo servidor do site
$dbName = 'u359247811_BD';
$dbUser = 'u359247811_Admin';
$dbPass = 'cP$6nHI6Pmm'; // coloque a senha do usuário MySQL
$port   = 3306;

$dsn = "mysql:host=$dbHost;port=$port;dbname=$dbName;charset=utf8mb4";

try {
    $pdo = new PDO($dsn, $dbUser, $dbPass, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ]);

    // Teste rápido: buscar 5 empresas
    $stmt = $pdo->query("SELECT * FROM empresas LIMIT 5");
    $empresas = $stmt->fetchAll();

    foreach ($empresas as $empresa) {
        echo htmlspecialchars($empresa['nome_empresa']) . "<br>";
    }
} catch (PDOException $e) {
    echo "Erro de conexão: " . $e->getMessage();
}
