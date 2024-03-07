- In jedes Model (z.B. TCNAE) sollen folgende Funktionen existieren:
  - ```train(data, lr = model_default, loss_func = model_default, opt_func = model_default)```
    - ```model_default``` ist der default Wert für das entsprechende Model (bei TCNAE z.B. Adam für opt_func)
  - ```predict(data)```
  - ```learner(data = None, lr = None, loss_func = None, opt_func = None)```
    - gibt den Learner (optional parametrisiert) von FastAI für das model zurück

## Fragen und Anmerkungen

- Was soll data sein (insbesondere in der predict Funktion)? Ein einzelnes Element/Zahl, um die automatisch ein Tensor etc. gewrapped wird? Ein DF? Ein Tensor? Ein Batched irgendwas?
- Brauchen wir weitere Funktionen für alle models?
- Kann man in Python auf schöne Art im Sinne von Objektorientierung die obigen Funktionen für alle models vorgeben?