# Política de Privacidade — Sugestor de Script (Clint)

Esta extensão é de uso interno do time de vendas do Grupo Primo, distribuída de forma privada apenas para contas do domínio corporativo timeprimo.com.

## O que a extensão lê e onde processa
- Campos de negócio do deal aberto no Clint (produto, origem, etapa, tags e campos customizados) -- para escolher o script de venda certo. Identificadores internos desses campos são enviados ao backend próprio do Grupo Primo (Supabase) para buscar o texto.
- O texto da última mensagem recebida em cada conversa da lista -- para classificá-la por cor. Lido e classificado dentro do navegador; o resultado é só o nome de uma cor. O texto não é armazenado, registrado em log nem enviado a nenhum servidor.
- O áudio de uma mensagem de voz, apenas quando o usuário clica em transcrever -- transcrito dentro do computador do usuário por um modelo empacotado na extensão. O áudio não sai do navegador; a transcrição fica guardada localmente (chrome.storage) para não repetir o trabalho.
- No discador: o nível de energia do áudio da ligação em curso, medido no navegador para detectar atendimento. O áudio da ligação não é gravado, transcrito nem enviado. O microfone é usado só porque a ligação é uma chamada de voz do vendedor.
- Nome, e-mail e telefone do contato trafegam nas respostas que o Clint já carrega normalmente; a extensão não guarda nem envia esses campos.

## O que a extensão escreve
- No campo de mensagem da tela do Clint: o texto do script escolhido (o envio continua manual).
- No CRM, apenas quando o vendedor envia o bloco "Desistência": marca o negócio como perdido e fecha a conversa, com as mesmas operações da tela e na sessão do próprio vendedor, após 6 segundos com opção de cancelar.
- No backend próprio (Supabase), no discador: a presença do vendedor na roda (nome e identificador do próprio vendedor, para o painel do supervisor) e o registro operacional de cada tentativa de ligação (identificador do negócio, horário, desfecho). Nenhum dado do lead: sem nome, telefone ou conteúdo.

## Retenção e terceiros
- Nenhum dado é enviado a terceiros além da infraestrutura do próprio Grupo Primo (Supabase) e do CRM Clint, que o vendedor já usa.
- A extensão não mantém histórico de conversas nem de deals visitados.

Contato: antonio.ribeiro@timeprimo.com

Última atualização: 10/09/2026 (versão 0.1.14 da extensão)
