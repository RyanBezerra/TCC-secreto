<?php
// Configurações de conexão com o banco de dados
// Banco hospedado no Hostinger
$dbHost = 'auth-db1524.hstgr.io';
$dbName = 'u359247811_BD';
$dbUser = 'u359247811_Admin';
$dbPass = 'cP$6nHI6Pmm';
$port = 3306;

$dsn = "mysql:host=$dbHost;port=$port;dbname=$dbName;charset=utf8mb4";

try {
    $pdo = new PDO($dsn, $dbUser, $dbPass, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_TIMEOUT => 10
    ]);
} catch (PDOException $e) {
    die("Erro de conexão: " . $e->getMessage());
}
?>