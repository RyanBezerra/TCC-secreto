<?php
require_once 'config.php';

// Definir header para JSON
header('Content-Type: application/json');

// Se for uma requisição AJAX para buscar empresas
if (isset($_GET['action']) && $_GET['action'] === 'get_empresas') {
    try {
        $stmt = $pdo->query("SELECT id, nome_empresa FROM empresas ORDER BY nome_empresa");
        $empresas = $stmt->fetchAll();
        echo json_encode($empresas);
        exit;
    } catch (PDOException $e) {
        echo json_encode(['error' => 'Erro ao carregar empresas: ' . $e->getMessage()]);
        exit;
    }
}

// Verificar se o formulário foi enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nome = trim($_POST['nome'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $senha = $_POST['senha'] ?? '';
    $cargo = trim($_POST['cargo'] ?? '');
    $empresa_nome = trim($_POST['empresa_nome'] ?? '');
    
    // Validações
    $erros = [];
    
    if (empty($nome)) {
        $erros[] = 'Nome é obrigatório';
    }
    
    if (empty($email)) {
        $erros[] = 'Email é obrigatório';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $erros[] = 'Email inválido';
    }
    
    if (empty($senha)) {
        $erros[] = 'Senha é obrigatória';
    } elseif (strlen($senha) < 6) {
        $erros[] = 'Senha deve ter pelo menos 6 caracteres';
    }
    
    if (empty($cargo)) {
        $erros[] = 'Cargo é obrigatório';
    }
    
    if (empty($empresa_nome)) {
        $erros[] = 'Empresa é obrigatória';
    } else {
        // Inicializar empresa_id
        $empresa_id = null;
        
        // Verificar se a empresa existe no banco ou criar uma nova
        try {
            $stmt = $pdo->prepare("SELECT id FROM empresas WHERE nome_empresa = ?");
            $stmt->execute([$empresa_nome]);
            $empresa_existente = $stmt->fetch();
            
            if ($empresa_existente) {
                $empresa_id = $empresa_existente['id'];
            } else {
                // Criar nova empresa se não existir
                // Usar o email do usuário como email de contato da empresa
                $stmt = $pdo->prepare("INSERT INTO empresas (nome_empresa, email_contato, data_cadastro) VALUES (?, ?, NOW())");
                $result = $stmt->execute([$empresa_nome, $email]);
                
                if (!$result) {
                    throw new Exception('Falha ao inserir empresa no banco');
                }
                
                $empresa_id = $pdo->lastInsertId();
                
                // Verificar se o ID foi gerado corretamente
                if (!$empresa_id || $empresa_id === 0) {
                    throw new Exception('Falha ao obter ID da empresa criada. ID retornado: ' . $empresa_id);
                }
            }
        } catch (PDOException $e) {
            $erros[] = 'Erro ao verificar/criar empresa: ' . $e->getMessage();
        }
    }
    
    // Verificar se email já existe
    if (empty($erros)) {
        try {
            $stmt = $pdo->prepare("SELECT id FROM usuarios WHERE email = ?");
            $stmt->execute([$email]);
            if ($stmt->fetch()) {
                $erros[] = 'Email já cadastrado';
            }
        } catch (PDOException $e) {
            $erros[] = 'Erro ao verificar email: ' . $e->getMessage();
        }
    }
    
    // Se não há erros, inserir no banco
    if (empty($erros)) {
        try {
            // Verificar se empresa_id foi definido
            if (!isset($empresa_id) || empty($empresa_id)) {
                throw new Exception('ID da empresa não foi definido');
            }
            
            // Debug: verificar valores antes da inserção
            $debug_values = [
                'empresa_id' => $empresa_id,
                'nome' => $nome,
                'email' => $email,
                'cargo' => $cargo
            ];
            
            // Verificar se algum valor está vazio
            foreach ($debug_values as $key => $value) {
                if (empty($value) && $value !== 0) {
                    throw new Exception("Campo '$key' está vazio: '$value'");
                }
            }
            
            $senha_hash = password_hash($senha, PASSWORD_DEFAULT);
            
            $stmt = $pdo->prepare("
                INSERT INTO usuarios (empresa_id, nome, email, senha_hash, cargo, status, data_cadastro) 
                VALUES (?, ?, ?, ?, ?, 'ativo', NOW())
            ");
            
            $stmt->execute([$empresa_id, $nome, $email, $senha_hash, $cargo]);
            
            echo json_encode([
                'success' => true,
                'message' => 'Usuário cadastrado com sucesso!'
            ]);
            exit;
            
        } catch (PDOException $e) {
            echo json_encode([
                'success' => false,
                'message' => 'Erro ao cadastrar usuário: ' . $e->getMessage()
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

// Se não for uma requisição POST, retornar erro
echo json_encode([
    'success' => false,
    'message' => 'Método não permitido'
]);
exit;
