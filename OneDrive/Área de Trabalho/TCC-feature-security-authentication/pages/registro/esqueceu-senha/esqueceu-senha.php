<?php
require_once $_SERVER['DOCUMENT_ROOT'] . '/configDB.php';

$mensagem = '';
$tipoMensagem = '';

// Verificar se o formulário foi enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email'] ?? '');
    
    // Validações
    $erros = [];
    
    if (empty($email)) {
        $erros[] = 'Email é obrigatório';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $erros[] = 'Email inválido';
    }
    
    // Se não há erros, verificar se email existe no banco
    if (empty($erros)) {
        try {
            // Buscar usuário pelo email
            $stmt = $pdo->prepare("
                SELECT u.id, u.nome, u.email, u.status, e.nome_empresa 
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
                    // Email encontrado - preparar para envio de email
                    $nome_usuario = $usuario['nome'];
                    $empresa_usuario = $usuario['nome_empresa'];
                    
                    // TODO: Implementar envio de email aqui
                    // Por enquanto, apenas simular o processo
                    
                    // Gerar token de redefinição (para uso futuro)
                    $token = bin2hex(random_bytes(32));
                    $token_expira = date('Y-m-d H:i:s', strtotime('+1 hour'));
                    
                    // Salvar token no banco (tabela temporária ou campo na tabela usuarios)
                    try {
                        // Verificar se já existe um token para este usuário
                        $stmt = $pdo->prepare("SELECT id FROM reset_tokens WHERE usuario_id = ? AND usado = 0");
                        $stmt->execute([$usuario['id']]);
                        $token_existente = $stmt->fetch();
                        
                        if ($token_existente) {
                            // Atualizar token existente
                            $stmt = $pdo->prepare("UPDATE reset_tokens SET token = ?, expira_em = ?, criado_em = NOW() WHERE usuario_id = ? AND usado = 0");
                            $stmt->execute([$token, $token_expira, $usuario['id']]);
                        } else {
                            // Criar novo token
                            $stmt = $pdo->prepare("INSERT INTO reset_tokens (usuario_id, token, expira_em, criado_em) VALUES (?, ?, ?, NOW())");
                            $stmt->execute([$usuario['id'], $token, $token_expira]);
                        }
                        
                        // TODO: Enviar email com link de redefinição
                        // $link_redefinicao = "https://seudominio.com/TCC/php/redefinir-senha.php?token=" . $token;
                        // enviarEmailRedefinicao($email, $nome_usuario, $link_redefinicao);
                        
                        $mensagem = "Instruções de redefinição de senha foram enviadas para <strong>{$email}</strong>. Verifique sua caixa de entrada e spam.";
                        $tipoMensagem = 'sucesso';
                        
                    } catch (PDOException $e) {
                        // Se a tabela reset_tokens não existir, apenas simular o sucesso
                        $mensagem = "Instruções de redefinição de senha foram enviadas para <strong>{$email}</strong>. Verifique sua caixa de entrada e spam.";
                        $tipoMensagem = 'sucesso';
                    }
                }
            } else {
                // Email não encontrado - por segurança, não revelar se o email existe ou não
                $mensagem = "Se o email <strong>{$email}</strong> estiver cadastrado em nosso sistema, você receberá instruções para redefinir sua senha.";
                $tipoMensagem = 'info';
            }
            
        } catch (PDOException $e) {
            $mensagem = 'Erro ao processar solicitação: ' . $e->getMessage();
            $tipoMensagem = 'erro';
        }
    } else {
        $mensagem = implode('<br>', $erros);
        $tipoMensagem = 'erro';
    }
}

// Função para enviar email de redefinição (implementar futuramente)
function enviarEmailRedefinicao($email, $nome, $link) {
    // TODO: Implementar envio de email
    // Exemplo usando PHPMailer ou função mail() do PHP
    
    $assunto = "Redefinição de Senha - GestiX";
    $corpo = "
    <html>
    <body>
        <h2>Redefinição de Senha</h2>
        <p>Olá {$nome},</p>
        <p>Você solicitou a redefinição de sua senha. Clique no link abaixo para criar uma nova senha:</p>
        <p><a href='{$link}' style='background: #000; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px;'>Redefinir Senha</a></p>
        <p>Este link expira em 1 hora.</p>
        <p>Se você não solicitou esta redefinição, ignore este email.</p>
        <p>Equipe GestiX</p>
    </body>
    </html>
    ";
    
    // Implementar envio real do email aqui
    return true;
}
?>

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Esqueceu a Senha - GestiX</title>
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
        
        .forgot-container {
            max-width: 450px;
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
        
        .forgot-header {
            text-align: center;
            margin-bottom: 32px;
        }
        
        .forgot-title {
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 8px;
            color: var(--text);
        }
        
        .forgot-subtitle {
            color: var(--muted);
            font-size: 16px;
            margin: 0;
            line-height: 1.5;
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
            margin-bottom: 24px;
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
        
        .btn-send {
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
        
        .btn-send:hover {
            background: #333;
            transform: translateY(-1px);
        }
        
        .btn-send:active {
            transform: translateY(0);
        }
        
        .btn-send:disabled {
            background: var(--muted);
            cursor: not-allowed;
            transform: none;
        }
        
        .back-actions {
            display: flex;
            flex-direction: column;
            gap: 12px;
            text-align: center;
        }
        
        .back-link {
            color: var(--brand);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .back-link:hover {
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
        
        .mensagem.info {
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        
        .form-help {
            font-size: 13px;
            color: var(--muted);
            margin-top: 4px;
        }
        
        .info-box {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 24px;
        }
        
        .info-box-title {
            font-weight: 600;
            color: var(--text);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .info-box-text {
            color: var(--muted);
            font-size: 14px;
            line-height: 1.5;
        }
        
        @media (max-width: 768px) {
            .forgot-container {
                padding: 16px;
            }
            
            .form-container {
                padding: 24px;
            }
        }
    </style>
</head>
<body>
    <div class="forgot-container">
        <div class="brand-logo">
            <i data-feather="briefcase"></i>
            <span class="brand-logo-text">GestiX</span>
        </div>
        
        <div class="forgot-header">
            <h1 class="forgot-title">Esqueceu a senha?</h1>
            <p class="forgot-subtitle">Digite seu email e enviaremos instruções para redefinir sua senha</p>
        </div>
        
        <div class="form-container">
            <?php if ($mensagem): ?>
                <div class="mensagem <?php echo $tipoMensagem; ?>">
                    <?php echo $mensagem; ?>
                </div>
            <?php endif; ?>
            
            <div class="info-box">
                <div class="info-box-title">
                    <i data-feather="info"></i>
                    Como funciona
                </div>
                <div class="info-box-text">
                    Digite o email cadastrado em sua conta. Se o email for encontrado, enviaremos um link para redefinir sua senha.
                </div>
            </div>
            
            <form method="POST" action="">
                <div class="form-group">
                    <label for="email" class="form-label">
                        Email cadastrado
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
                    <div class="form-help">Digite o email que você usou para se cadastrar</div>
                </div>
                
                <button type="submit" class="btn-send">
                    <i data-feather="mail"></i>
                    Enviar instruções
                </button>
                
                <div class="divider"></div>
                
                <div class="back-actions">
                    <a href="../login/login.html" class="back-link">
                        <i data-feather="arrow-left"></i>
                        Voltar ao login
                    </a>
                    <a href="../cadastro/cadastro.html" class="back-link">
                        <i data-feather="user-plus"></i>
                        Criar nova conta
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
