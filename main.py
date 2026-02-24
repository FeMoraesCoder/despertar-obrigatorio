import time
import tinytuya
import os
from dotenv import load_dotenv

class LampaDespertador:
    def __init__(self, device_id, ip_address, local_key, version=3.3):
        """
        Inicializa a conexão com a lâmpada Positivo/Tuya.
        """
        self.lampa = tinytuya.BulbDevice(
            dev_id=device_id,
            address=ip_address,
            local_key=local_key,
            version=version
        )
        # Mantém o socket aberto para comandos em sequência (evita lag)
        self.lampa.set_socketPersistent(True)
        
        # Testa a conexão obtendo o status atual
        self.status = self.lampa.status()
        print(f"Lâmpada conectada. Status inicial: {self.status}")

def iniciar_despertar_suave(self, duracao_minutos=10):
        """
        Fase 1: Liga a lâmpada em 1% com cor quente e sobe até 100%.
        """
        print(f"Iniciando Fase 1: Despertar Suave ({duracao_minutos} minutos)...")
        
        self.lampa.turn_on()
        self.lampa.set_mode('white')
        
        # Em set_white_percentage, os valores devem ser estritamente entre 0 e 100.
        # 100 para temperatura de cor geralmente significa o tom mais quente (amarelo/laranja).
        # Se na sua lâmpada 100 ficar muito azul (frio), mude para 0.
        temp_cor = 100 
        
        passos = 100
        # Divide o tempo total em segundos por 100 passos
        espera_por_passo = (duracao_minutos * 60) / passos 
        
        # Loop limpo de 1 a 100 por cento
        for brilho in range(1, 101):
            status_atual = self.lampa.status()
            
            # Interrupção de segurança: verificar se o usuário desligou no interruptor ou app
            # O DPS '20' é o booleano que indica se a lâmpada está ligada (True) ou desligada (False)
            if not status_atual.get('dps', {}).get('20'): 
                print("\nInterrupção detectada! Lâmpada desligada manualmente. Bom dia!")
                return False
                
            self.lampa.set_white_percentage(brilho, temp_cor)
            time.sleep(espera_por_passo)
            
        print("\nFase 1 concluída.")
        return True

def ativar_modo_insuportavel(self, timeout_minutos=5):
        """
        Fase 2: Alerta Crítico. Loop de strobo vermelho e azul no brilho máximo.
        """
        print("Iniciando Fase 2: MODO INSUPORTÁVEL!")
        
        tempo_fim = time.time() + (timeout_minutos * 60)
        
        while time.time() < tempo_fim:
            # Atenção: não coloque sleeps muito pequenos (menores que 0.5s) 
            # para não travar o microcontrolador (MCU) da lâmpada com excesso de requisições.
            self.lampa.set_colour(r=255, g=0, b=0) # Vermelho
            time.sleep(1)
            self.lampa.set_colour(r=0, g=0, b=255) # Azul
            time.sleep(1)
            
        print("Fim do modo insuportável.")
        self.lampa.turn_off()

# ==========================================
# Exemplo de Uso
# ==========================================
if __name__ == "__main__":
    # Carrega as variáveis de segurança do arquivo .env
    load_dotenv()

    DEVICE_ID = os.getenv("BULB_DEVICE_ID")
    IP_ADDRESS = os.getenv("BULB_IP")
    LOCAL_KEY = os.getenv("BULB_LOCAL_KEY")

    if not all([DEVICE_ID, IP_ADDRESS, LOCAL_KEY]):
        print("Erro: Credenciais não encontradas. Verifique seu arquivo .env")
        exit(1)

    print("Iniciando rotina do Despertar Obrigatório...")
    despertador = LampaDespertador(DEVICE_ID, IP_ADDRESS, LOCAL_KEY)
    
    # Execução das fases (ajustei para tempos curtos para você testar agora)
    print("Iniciando teste da Fase 1 (1 minuto)...")
    se_nao_acordou = despertador.iniciar_despertar_suave(duracao_minutos=1) 
    
    if se_nao_acordou:
        print("Usuário não desligou a lâmpada. Acionando Fase 2!")
        # 30 segundos de strobo vermelho e azul para testar
        despertador.ativar_modo_insuportavel(timeout_minutos=0.5)