# AeroOps
Plataforma mundial de análise histórica de dados aeronáuticos.

## Objetivo
Criar um dashboard web para consultar, visualizar e analisar dados públicos de aeronaves, aeroportos, trajetórias e condições meteorológicas, sem depender de APIs pagas.

## Escopo inicial
A primeira versão deverá permitir:
- consultar aeroportos do mundo;
- visualizar pistas e informações básicas;
- importar dados públicos de aeronaves;
- armazenar dados históricos de posições;
- consultar trajetórias;
- exibir mapas e gráficos;
- mostrar indicadores por país e aeroporto;
- atualizar os dados periodicamente;
- funcionar em uma VPS Hostinger;
- utilizar PostgreSQL;
- executar com Docker Compose.

## Fora do escopo inicial
- controle de aeronaves;
- decisões de voo;
- sistema certificado de segurança;
- acompanhamento em tempo real;
- uso obrigatório de APIs pagas;
- venda de dados;
- substituição de sistemas oficiais de aviação.

## Fontes iniciais de dados
- OurAirports;
- OpenSky Network dentro dos limites gratuitos;
- Open-Meteo;
- dados públicos adicionais compatíveis com o projeto.

## Arquitetura planejada
- Front-end web;
- API FastAPI;
- PostgreSQL;
- Docker Compose;
- VPS Hostinger;
- GitHub Actions;
- atualizações periódicas por tarefas agendadas.

## Regra de custo
O projeto utilizará software e dados gratuitos. O único custo obrigatório inicial será a VPS da Hostinger.

## Aviso
O AeroOps é um projeto educacional e analítico. Seus dados não devem ser usados como única fonte para decisões reais de voo, navegação ou segurança operacional.