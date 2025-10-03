<?php
/**
 * Dashboard com verificação de autenticação
 * Protege o acesso baseado na tabela log
 */

require_once '../../auth.php';

// Verificar autenticação - redireciona para login se não autenticado
$auth->requireAuth();

// Registrar acesso ao dashboard
$user = $auth->getCurrentUser();
$auth->logActivity($user['id'], 'dashboard_acesso', 'Acesso ao dashboard principal');

?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard - GestiX</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/index.css">
</head>
<body>
  <div class="app"> 
    <aside class="sidebar">
      <div class="brand">
        <i data-feather="briefcase"></i>
        <div class="brand-text">
          <span class="brand-title">GestiX</span>
          <span class="brand-sub">Sistema Inteligente</span>
        </div>
      </div>
      <nav class="nav">
        <a class="active" href="#"><i data-feather="home"></i>Dashboard</a>
        <a href="../cronograma/cronograma.html"><i data-feather="calendar"></i>Cronograma</a>
        <a href="../agendamentos/agendamentos.html"><i data-feather="users"></i>Agendamentos</a>
        <a href="../insights/insights.html"><i data-feather="cpu"></i>Insights IA</a>
        <a href="../registro/cadastro/cadastro.html"><i data-feather="user-plus"></i>Cadastro</a>
      </nav>
      <div class="sidebar-footer">
        <a href="#" class="nav-link sidebar-settings-link"><i data-feather="settings"></i>Configurações</a>
        <a href="#" onclick="logout()" class="nav-link"><i data-feather="log-out"></i>Sair</a>
      </div>
    </aside>

    <main class="content">
      <div class="content-header">
        <div>
          <h1 class="page-title">Dashboard</h1>
          <p class="page-sub">Visão geral das operações da sua empresa</p>
        </div>
        <div class="user-info">
          <span>Bem-vindo, <?php echo htmlspecialchars($user['nome']); ?>!</span>
          <span class="user-role"><?php echo ucfirst($user['cargo']); ?></span>
        </div>
      </div>

      <section class="grid grid-top">
        <div class="card">
          <div class="kpi-title metric-title"><i data-feather="user"></i>Funcionários Ativos</div>
          <p class="kpi-value">24</p>
          <div class="kpi-sub">+2 esta semana</div>
        </div>
        <div class="card">
          <div class="kpi-title metric-title"><i data-feather="calendar"></i>Agendamentos Hoje</div>
          <p class="kpi-value">18</p>
          <div class="meta">3 pendentes</div>
        </div>
        <div class="card">
          <div class="kpi-title metric-title"><i data-feather="trending-up"></i>Taxa de Ocupação</div>
          <p class="kpi-value">85%</p>
          <div class="kpi-sub">+5% vs mês anterior</div>
        </div>
        <div class="card">
          <div class="kpi-title metric-title"><i data-feather="alert-triangle"></i>Alertas Ativos</div>
          <p class="kpi-value">3</p>
          <div class="meta">2 críticos</div>
        </div>
      </section>

      <section class="grid grid-main mt-16">
        <div class="card">
          <div class="kpi-title mb-12"><i data-feather="clock"></i>Atividades Recentes</div>
          <div class="list">
            <div class="list-item">
              <span class="dot green"></span>
              <div>
                <div>João Silva adicionado ao turno da manhã</div>
                <div class="meta">10:30</div>
              </div>
            </div>
            <div class="list-item">
              <span class="dot blue"></span>
              <div>
                <div>Novo agendamento: Maria Santos - 14:00</div>
                <div class="meta">09:15</div>
              </div>
            </div>
            <div class="list-item">
              <span class="dot amber"></span>
              <div>
                <div>Conflito de horário detectado no setor A</div>
                <div class="meta">08:45</div>
              </div>
            </div>
            <div class="list-item">
              <span class="dot blue"></span>
              <div>
                <div>Ana Lima cancelou agendamento para amanhã</div>
                <div class="meta">07:55</div>
              </div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="kpi-title mb-12"><i data-feather="check-circle"></i>Insights da IA</div>
          <div class="list">
            <div class="insight">
              <span class="tag gray">Otimização</span>
              <div>Sugestão: Redistribuir 2 funcionários do turno da tarde para manhã para melhor cobertura.</div>
            </div>
            <div class="insight">
              <span class="tag yellow">Previsão</span>
              <div>Tendência: Aumento de 15% nos agendamentos previsto para próxima semana.</div>
            </div>
            <div class="insight">
              <span class="tag red">Alerta</span>
              <div>Conflito: Dois agendamentos simultâneos detectados para terça-feira às 15:00.</div>
            </div>
            <div class="insight">
              <span class="tag gray">Eficiência</span>
              <div>Recomendação: Implementar turno noturno para reduzir sobrecarga diurna em 20%.</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
  
  <script src="https://unpkg.com/feather-icons"></script>
  <script src="/index.js"></script>
  <script>
    // Função de logout
    function logout() {
      if (confirm('Tem certeza que deseja sair?')) {
        fetch('../../logout.php', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          }
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            window.location.href = '../registro/login/login.html';
          } else {
            alert('Erro ao fazer logout: ' + data.message);
          }
        })
        .catch(error => {
          console.error('Erro:', error);
          // Redirecionar mesmo com erro
          window.location.href = '../registro/login/login.html';
        });
      }
    }
    
    // Verificar sessão periodicamente (a cada 5 minutos)
    setInterval(function() {
      fetch('../../check_session.php')
        .then(response => response.json())
        .then(data => {
          if (!data.valid) {
            alert('Sua sessão expirou. Faça login novamente.');
            window.location.href = '../registro/login/login.html';
          }
        })
        .catch(error => {
          console.error('Erro ao verificar sessão:', error);
        });
    }, 300000); // 5 minutos
  </script>
</body>
</html>
