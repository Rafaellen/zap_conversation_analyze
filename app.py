import pandas as pd
import os
import matplotlib.pyplot as plt

def analysis_zap_group(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = []
    for line in lines:
        if '] ' in line:
            date_time, message = line.split('] ', 1)
            date_time = date_time[1:].strip('[')
            date, time = date_time.split(', ')
            if ': ' in message:
                name, message = message.split(': ', 1)
                data.append([date.strip(), time.strip(), name.strip(), message.strip()])
    
    df = pd.DataFrame(data, columns=['data', 'hora', 'remetente', 'mensagem'])
    return df

def resume(df):
    summary_df = df['remetente'].value_counts().reset_index()
    summary_df.columns = ['Remetente', 'Total de Mensagens']
    print("\nResumo das Conversas:")
    print(summary_df)

def sender_history(df, sender):
    sender_df = df[df['remetente'] == sender]
    print(f"\nHistórico de Mensagens de {sender}:")
    if not sender_df.empty:
        print(sender_df)
    else:
        print("Nenhuma mensagem encontrada para este remetente.")

def graph_sender_history_line(df):
    df['data'] = df['data'].str.strip()
    df['hora'] = df['hora'].str.strip()
    
    try:
        df['data'] = pd.to_datetime(df['data'] + ' ' + df['hora'], dayfirst=True)
    except ValueError as e:
        print("Erro ao converter datas:", e)
        return
    
    sender_counts = df.groupby([df['data'].dt.date, 'remetente']).size().unstack(fill_value=0)
    
    plt.figure(figsize=(12, 6))
    sender_counts.plot(kind='line', marker='o', color=plt.cm.tab10.colors)
    
    plt.title('Mensagens por Dia para Cada Remetente')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de Mensagens')
    plt.xticks(rotation=45)
    plt.legend(title='Remetente')
    plt.tight_layout()
    plt.show()

def graph_sender_history_bar(df):
    try:
        df['data'] = pd.to_datetime(df['data'] + ' ' + df['hora'], dayfirst=True)
        
        sender_counts = df.groupby([df['data'].dt.date, 'remetente']).size().unstack(fill_value=0)
        
        plt.figure(figsize=(12, 6))
        sender_counts.plot(kind='bar', stacked=True, color=plt.cm.tab10.colors)
        
        plt.title('Mensagens por Dia para Cada Remetente')
        plt.xlabel('Data')
        plt.ylabel('Quantidade de Mensagens')
        plt.xticks(rotation=45)
        plt.legend(title='Remetente', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
    
    except ValueError as e:
        print("Erro ao converter datas:", e)

def graph_pizza(df):
    plt.figure(figsize=(8, 8))
    df['remetente'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribuição de Mensagens por Remetente')
    plt.ylabel('')
    plt.show()

def main(file_path):
    if os.path.exists(file_path):
        df = analysis_zap_group(file_path)
        print("\Arquivo de Mensagens:")
        print(df)

        while True:
            print("\nBem-vindo ao Chat Analista do ZapZap!")
            print("\nEscolha uma opção:")
            print("1. Resumo das conversas")
            print("2. Histórico de um remetente")
            print("3. Gráfico de linhas do histórico de mensagens por dia")
            print("4. Gráfico de barras da quantidade de mensagens por dia")
            print("5. Gráfico de pizza dos remetentes e suas mensagens enviadas ")
            print("6. Sair")
            choice = input("Digite sua escolha: ")

            if choice == '1':
                resume(df)
            elif choice == '2':
                sender = input("Digite o nome do remetente: ")
                if sender in df['remetente'].values:
                    sender_history(df, sender)
                else:
                    print("Remetente não encontrado.")
            elif choice == '3':
                graph_sender_history_line(df)
            elif choice == '4':
                graph_sender_history_bar(df)
            elif choice == '5':
                graph_pizza(df)
            elif choice == '6':
                print("Saindo...")
                break
            else:
                print("Escolha inválida. Tente novamente.")
    else:
        print("Arquivo não encontrado. Verifique o caminho e tente novamente.")

if __name__ == '__main__':
    file = 'caminho_do_arquivo.txt'
    main(file)
