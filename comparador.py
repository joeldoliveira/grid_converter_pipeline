import pandas as pd
import matplotlib.pyplot as plt

#ler os ficheiros
df1 = pd.read_csv("dados_mat.csv", header=None)
df2 = pd.read_csv("dados_power.csv", header=None)

#Definir colunas
df1.columns = ["bus", "V1", "angle1", "pload1", "qload1"]
df2.columns = ["bus", "V2", "angle2", "pload2", "qload2"]

df1["bus"] = df1["bus"].astype(int)
df2["bus"] = df2["bus"].astype(int)

df = pd.merge(df1, df2, on="bus")
# print(df)

###Tensão
plt.figure()
plt.plot(df["bus"], df["V1"], marker='o', label="dados_mat")
plt.plot(df["bus"], df["V2"], marker='x', label="dados_power")

df["erro_V_percent"] = abs((df["V1"] - df["V2"]) / df["V2"])*100
erro_medio_V = df["erro_V_percent"].mean()

plt.xlabel("Barramento")
plt.ylabel("Magnitude")
plt.title("Comparação")
plt.text(
    0.005, 0.95,
    f"Erro médio: {erro_medio_V:.2f}%\n",
    transform=plt.gca().transAxes,
    verticalalignment='top'
)
plt.legend()
plt.grid()

###Ângulo
plt.figure()
plt.plot(df["bus"], df["angle1"], marker='o', label="dados_mat")
plt.plot(df["bus"], df["angle2"], marker='x', label="dados_power")

df["erro_ang_percent"] = abs((df["angle2"] - df["angle1"]) / df["angle1"])*100
erro_medio_ang = df["erro_ang_percent"].mean()

plt.xlabel("Barramento")
plt.ylabel("Ângulo")
plt.title("Comparação")
plt.text(
    0.005, 0.95,
    f"Erro médio: {erro_medio_ang:.2f}%\n",
    transform=plt.gca().transAxes,
    verticalalignment='top'
)
plt.legend()
plt.grid()


#Calcular erros de tensão e de ângulo
df["erro_V"] = df["V1"] - df["V2"]
df["erro_angle"] = df["angle1"] - df["angle2"]

plt.figure()
plt.bar(df["bus"], df["erro_V"])
plt.xlabel("Barramento")
plt.ylabel("Erro de Tensão")
plt.title("Erro de Tensão")
plt.grid()

plt.figure()
plt.bar(df["bus"], df["erro_angle"])
plt.xlabel("Barramento")
plt.ylabel("Erro de Ângulo")
plt.title("Erro de Ângulo")
plt.grid


###Potencia ativa
plt.figure()
plt.plot(df["bus"], df["pload1"], marker='o', label="dados_mat")
plt.plot(df["bus"], df["pload2"], marker='x', label="dados_power")

df["erro_pload_percent"] = abs((df["pload1"] - df["pload2"]) / df["pload2"])*100
erro_medio_pload = df["erro_pload_percent"].mean()

plt.xlabel("Barramento")
plt.ylabel("Potência Ativa")
plt.title("Comparação")
plt.text(
    0.005, 0.95,
    f"Erro médio: {erro_medio_pload:.2f}%\n",
    transform=plt.gca().transAxes,
    verticalalignment='top'
)
plt.legend()
plt.grid()

###Potencia reativa
plt.figure()
plt.plot(df["bus"], df["qload1"], marker='o', label="dados_mat")
plt.plot(df["bus"], df["qload2"], marker='x', label="dados_power")

df["erro_qload_percent"] = abs((df["qload1"] - df["qload2"]) / df["qload2"])*100
erro_medio_qload = df["erro_qload_percent"].mean()

plt.xlabel("Barramento")
plt.ylabel("Potência Reativa")
plt.title("Comparação")
plt.text(
    0.005, 0.95,
    f"Erro médio: {erro_medio_qload:.2f}%\n",
    transform=plt.gca().transAxes,
    verticalalignment='top'
)
plt.legend()
plt.grid()

#Calcular erros de potência ativa e reativa
df["erro_pload"] = df["pload1"] - df["pload2"]
df["erro_qload"] = df["qload1"] - df["qload2"]

plt.figure()
plt.bar(df["bus"], df["erro_pload"])
plt.xlabel("Barramento")
plt.ylabel("Erro de Potência Ativa")
plt.title("Erro de Potência Ativa")
plt.grid()

plt.figure()
plt.bar(df["bus"], df["erro_qload"])
plt.xlabel("Barramento")
plt.ylabel("Erro de Potência Reativa")
plt.title("Erro de Potência Reativa")
plt.grid



plt.show()