## Voter
Definimos um "voter" como sendo um componente de um sistema distribuído que espera receber ve mensagens de entrada em um período de tempo máximo to e produz como saída um veredito correspondente à mensagem da maioria ou inconclusivo quando não houver maioria.

### Especificação
O voter aguarda por ve mensagens (ve é parâmetro do programa). Ao receber a primeira mensagem, um timeout to deve ser agendado (to também é parâmetro do programa). Se recebe ve mensagens antes do fim do timeout, produz veredito e cancela timeout. A maioria aqui é computada em Python por math.ceil((ve+1)/2).

Se to expira, contabiliza o número de mensagens recebidas vr (vr <= ve) e produz veredito com base na maioria de vr. A maioria agora é sobre as mensagens recebidas (vr) e não sobre as mensagens esperadas (ve): math.ceil((vr+1)/2).

### Implementação
- Utilize a plataforma Pyro5Links para um site externo. para a sua implementação.

- A saída do voter pode ser feita na tela.

- As mensagens de entrada do voter chegam por invocação do método send(msg) na sua interface (via Pyro5).

- Crie programa cliente que chame o método remoto send() para os seguintes casos:
  1. ve mensagens chegam → produz veredito com a maioria;
  2. vr < ve mensagens chegam → produz veredito com a maioria;
  3. produz veredito inconclusivo (nos casos 1 e 2 acima).
