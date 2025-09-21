<?php
session_start();
require_once 'config.php';

$mensagem = '';
$tipoMensagem = '';

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
                    $mensagem = 'Sua conta está inativa. Entre em contato com o administrador.';
                    $tipoMensagem = 'erro';
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
                        
                        // Atualizar último acesso
                        $stmt = $pdo->prepare("UPDATE usuarios SET ultimo_acesso = NOW() WHERE id = ?");
                        $stmt->execute([$usuario['id']]);
                        
                        // Redirecionar para a página de cadastro
                        header('Location: ../html/cadastro.html');
                        exit;
                    } else {
                        $mensagem = 'Senha incorreta';
                        $tipoMensagem = 'erro';
                    }
                }
            } else {
                $mensagem = 'Email não encontrado';
                $tipoMensagem = 'erro';
            }
            
        } catch (PDOException $e) {
            $mensagem = 'Erro ao verificar credenciais: ' . $e->getMessage();
            $tipoMensagem = 'erro';
        }
    } else {
        $mensagem = implode('<br>', $erros);
        $tipoMensagem = 'erro';
    }
}

// Se já estiver logado, redirecionar
if (isset($_SESSION['logado']) && $_SESSION['logado'] === true) {
    header('Location: ../html/cadastro.html');
    exit;
}
?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - GestiX</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root { 
            --bg: #ffffff; 
            --panel: #f8f9fa; 
            --muted: #6c757d; 
            --text: #212529; 
            --brand: #000000; 
            --ok: #28a745; 
            --warn: #ffc107; 
            --alert: #dc3545; 
            --card: #ffffff; 
            --border: #dee2e6; 
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, Arial, sans-serif;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text);
        }
        
        .login-container {
            max-width: 400px;
            width: 100%;
            padding: 24px;
        }
        
        .brand-logo {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin-bottom: 24px;
        }
        
        .brand-logo i {
            width: 40px;
            height: 40px;
            color: var(--brand);
        }
        
        .brand-logo-text {
            font-size: 24px;
            font-weight: 700;
            color: var(--brand);
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 32px;
        }
        
        .login-title {
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 8px;
            color: var(--text);
        }
        
        .login-subtitle {
            color: var(--muted);
            font-size: 16px;
            margin: 0;
        }
        
        .form-container {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 32px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 20px;
        }
        
        .form-label {
            font-weight: 600;
            color: var(--text);
            font-size: 14px;
        }
        
        .form-label .required {
            color: var(--alert);
            margin-left: 4px;
        }
        
        .form-input {
            padding: 12px 16px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 16px;
            background: var(--bg);
            color: var(--text);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        
        .form-input:focus {
            outline: none;
            border-color: var(--brand);
            box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1);
        }
        
        .btn-login {
            width: 100%;
            padding: 16px;
            background: var(--brand);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s ease, transform 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-bottom: 20px;
        }
        
        .btn-login:hover {
            background: #333;
            transform: translateY(-1px);
        }
        
        .btn-login:active {
            transform: translateY(0);
        }
        
        .login-actions {
            display: flex;
            flex-direction: column;
            gap: 12px;
            text-align: center;
        }
        
        .login-link {
            color: var(--brand);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.2s ease;
        }
        
        .login-link:hover {
            color: #333;
            text-decoration: underline;
        }
        
        .divider {
            height: 1px;
            background: var(--border);
            margin: 20px 0;
            position: relative;
        }
        
        .divider::after {
            content: 'ou';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: var(--card);
            padding: 0 12px;
            color: var(--muted);
            font-size: 12px;
        }
        
        .mensagem {
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 24px;
            text-align: center;
            font-weight: 500;
        }
        
        .mensagem.sucesso {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .mensagem.erro {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .form-help {
            font-size: 13px;
            color: var(--muted);
            margin-top: 4px;
        }
        
        @media (max-width: 768px) {
            .login-container {
                padding: 16px;
            }
            
            .form-container {
                padding: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="brand-logo">
            <i data-feather="briefcase"></i>
            <span class="brand-logo-text">GestiX</span>
        </div>
        
        <div class="login-header">
            <h1 class="login-title">Bem-vindo de volta</h1>
            <p class="login-subtitle">Faça login para acessar sua conta</p>
        </div>
        
        <div class="form-container">
            <?php if ($mensagem): ?>
                <div class="mensagem <?php echo $tipoMensagem; ?>">
                    <?php echo $mensagem; ?>
                </div>
            <?php endif; ?>
            
            <form method="POST" action="">
                <div class="form-group">
                    <label for="email" class="form-label">
                        Email
                        <span class="required">*</span>
                    </label>
                    <input 
                        type="email" 
                        id="email" 
                        name="email" 
                        class="form-input" 
                        required
                        placeholder="Digite seu email"
                        autocomplete="email"
                        value="<?php echo htmlspecialchars($email ?? ''); ?>"
                    >
                    <div class="form-help">Digite o email cadastrado</div>
                </div>
                
                <div class="form-group">
                    <label for="senha" class="form-label">
                        Senha
                        <span class="required">*</span>
                    </label>
                    <input 
                        type="password" 
                        id="senha" 
                        name="senha" 
                        class="form-input" 
                        required
                        placeholder="Digite sua senha"
                        autocomplete="current-password"
                    >
                    <div class="form-help">Digite sua senha de acesso</div>
                </div>
                
                <button type="submit" class="btn-login">
                    <i data-feather="log-in"></i>
                    Entrar
                </button>
                
                <div class="divider"></div>
                
                <div class="login-actions">
                    <a href="../html/cadastro.html" class="login-link">
                        <i data-feather="user-plus"></i>
                        Criar nova conta
                    </a>
                    <a href="esqueceu-senha.php" class="login-link">
                        <i data-feather="help-circle"></i>
                        Esqueceu a senha?
                    </a>
                </div>
            </form>
        </div>
    </div>

    <script src="https://unpkg.com/feather-icons"></script>
    <script>
        // Inicializar ícones
        feather.replace();
        
    </script>
</body>
</html>
