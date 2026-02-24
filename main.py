import os
import time
import tinytuya
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
        self.lampa.set_socketPersistent(True)
        
        self.status = self.lampa.status()
        print(f"Lâmpada conectada. Status inicial: {self.status}")

    def iniciar_despertar_suave(self, duracao_minutos=10):
        """
        Fase 1: Liga a lâmpada em 1% com cor quente e sobe até 100%.
        """
        print(f"Iniciando Fase 1: Despertar Suave ({duracao_minutos} minutos)...")
        
        self.lampa.turn_on()
        self.lampa.set_mode('white')
        
        temp_cor = 100 # 100 costuma ser a cor mais quente (amarelada)
        passos = 100
        espera_por_passo = (duracao_minutos * 60) / passos 
        
        for brilho in range(1, 101):
            status_atual = self.lampa.status()
            
            # DPS 20 = On/Off status
            if not status_atual.get('dps', {}).get('20'): 
                print("\nInterrupção detectada! Lâmpada desligada manualmente. Bom dia!")
                return False
                
            self.lampa.set_white_percentage(brilho, temp_cor)
            time.sleep(espera_por_passo)
            
        print("\nFase 1 concluída.")
        return True

    def ativar_modo_insuportavel(self, timeout_minutos=5):
        """
        Fase 2: Alerta Crítico. Loop de strobo vermelho e azul.
        """
        print("Iniciando Fase 2: MODO INSUPORTÁVEL!")
        
        tempo_fim = time.time() + (timeout_minutos * 60)
        
        while time.time() < tempo_fim:
            self.lampa.set_colour(r=255, g=0, b=0)
            time.sleep(1)
            self.lampa.set_colour(r=0, g=0, b=255)
            time.sleep(1)
            
        print("Fim do modo insuportável.")
        self.lampa.turn_off()


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
    
    print("Iniciando teste da Fase 1 (1 minuto)...")
    se_nao_acordou = despertador.iniciar_despertar_suave(duracao_minutos=1) 
    
    if se_nao_acordou:
        print("Usuário não desligou a lâmpada. Acionando Fase 2!")
        despertador.ativar_modo_insuportavel(timeout_minutos=0.5)