# Import libraries
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Creates a pie chart based on 3 int values 
def plot(pos: int, neg: int, nu: int, container):
    # Remove old chart if needed
    for widget in container.winfo_children():
        widget.destroy()

    # Creating dataset
    labels = ['Positive:\n {}'.format(pos), 'Negative:\n {}'.format(neg), 'Neutral:\n {}'.format(nu)]
    data = [pos, neg, nu]
    explode = [0.2 if x == max(data) else 0.0 for x in data]

    # Create Matplotlib figure
    fig = Figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    wedges, texts, autotexts = ax.pie(data, labels=labels, explode=explode, shadow=True, autopct='%1.1f%%')
    ax.legend(wedges, labels, title="Sentiment", loc="upper left", bbox_to_anchor=(1, 1))

    # Embed plot in tkinter
    canvas = FigureCanvasTkAgg(fig, master=container)
    canvas.draw()
    canvas.get_tk_widget().pack()


def total(pos:int, neg:int, nu:int):
    print(pos + neg + nu)