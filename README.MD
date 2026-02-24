# Despertar Obrigatório 💡⏰

Um script em Python para assumir o controle local de lâmpadas inteligentes (ecossistema Tuya / Positivo) e criar um despertador à prova de falhas e autossabotagem. 

O aplicativo oficial limita as automações. Este projeto utiliza a biblioteca `tinytuya` para enviar comandos locais via rede Wi-Fi, garantindo um despertar suave e, se necessário, métodos extremos para forçar o usuário a sair da cama.

## 🚀 Funcionalidades Atuais

* **Fase 1 - Despertar Suave:** Inicia a lâmpada em 1% de brilho (cor quente) e aumenta gradativamente até 100% durante o tempo estipulado.
* **Sistema Antifraude:** Se o usuário tentar apagar a lâmpada pelo interruptor ou aplicativo durante o despertar, o script detecta a queda de status e religa a luz imediatamente na cara do usuário.
* **Fase 2 - Modo Insuportável:** Se o alarme não for desarmado a tempo, a lâmpada entra em um loop de *strobo* policial (vermelho e azul no brilho máximo).
* **Desarme Inteligente:** Para parar o alarme (Fase 1) ou o strobo (Fase 2), o usuário é obrigado a interagir com o aplicativo e mudar os modos de iluminação (Cor/Branco), travando a lâmpada em luz branca fria (100%) para inibir a melatonina.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **tinytuya:** Para comunicação na rede local com dispositivos do ecossistema Tuya.
* **python-dotenv:** Para gerenciamento seguro de credenciais locais.

## ⚙️ Como Configurar e Rodar (Linux/Fedora)

1. Clone este repositório:
   ```bash
   git clone git@github.com:seu_usuario/despertar-obrigatorio.git
   cd despertar-obrigatorio
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install tinytuya python-dotenv
   ```

4. **Extração das Chaves:** Você precisará criar um projeto na [Tuya IoT Platform](https://iot.tuya.com/) e usar o `tinytuya wizard` para extrair o Device ID, IP Local e a Local Key da sua lâmpada.

5. Crie um arquivo `.env` na raiz do projeto e insira as suas credenciais (este arquivo é ignorado pelo Git por segurança):
   ```env
   BULB_DEVICE_ID=seu_device_id
   BULB_IP=192.168.0.X
   BULB_LOCAL_KEY=sua_local_key
   ```

6. Execute o script:
   ```bash
   python main.py
   ```

## 🗺️ Roadmap e Melhorias Futuras

As próximas implementações serão gerenciadas via [Issues](../../issues) neste repositório:

- [ ] **Agendamento Automático (CRON):** Configurar a execução do script no sistema operacional (via `cron` no Linux) para rodar automaticamente nos horários definidos.
- [ ] **Inteligência de Calendário:** Integrar uma API de Feriados Nacionais/Regionais para validar dias úteis. O script deve decidir sozinho se deve ou não tocar.
- [ ] **Desarme Físico (Tag NFC):** Criar uma rota web local (via Flask ou FastAPI) para desarmar o alarme apenas quando o celular for aproximado de uma Tag NFC colada no espelho do banheiro.
- [ ] **Desarme via QR Code:** Alternativa ao NFC, forçando a leitura de um QR Code impresso em outro cômodo.
- [ ] **Integração Climática:** Ajustar a temperatura da luz do despertar baseado na temperatura externa via API de clima (ex: dias muito frios ou chuvosos recebem uma luz um pouco mais quente e prolongada).