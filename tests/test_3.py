import matplotlib.pyplot as plt
import networkx as nx
from humanity import Humanity
from matplotlib.gridspec import GridSpec
import random
from matplotlib.widgets import Button

class Simulation:
    def __init__(self):
        self.humanity = Humanity()
        self.humanity.MIN_TRIBE_SIZE = 15
        self.humanity.LEADER_MIN_AGE = 45
        self.year = 0
        self.population_history = []
        
        # Konfiguracja okna
        plt.ion()
        self.fig = plt.figure(figsize=(20, 12))
        self.fig.canvas.manager.set_window_title('Symulacja społeczeństwa')
        
        # Układ wykresów z miejscem na przycisk
        gs = GridSpec(4, 3, figure=self.fig, height_ratios=[8, 8, 2, 1])
        self.ax_society = self.fig.add_subplot(gs[:2, :2])
        self.ax1 = self.fig.add_subplot(gs[0, 2])
        self.ax2 = self.fig.add_subplot(gs[1, 2])
        self.ax3 = self.fig.add_subplot(gs[2, :])
        self.ax_button = self.fig.add_subplot(gs[3, :])
        
        # Dodanie przycisku
        self.button = Button(self.ax_button, 'Następny rok')
        self.button.on_clicked(self.on_button_click)
        
    def run(self):
        """Uruchamia symulację i utrzymuje okno otwarte"""
        # Inicjalizacja wyświetlania
        self.update_society_graph()
        self.update_statistics()
        self.fig.tight_layout()
        
        # Konfiguracja zamykania okna
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        
        # Wyświetlenie okna
        plt.show(block=True)

    def on_button_click(self, event):
        self.run_simulation_step()
        self.print_info()

    def print_info(self):
        """Drukuje informacje o społeczeństwie w bardziej zwięzły sposób"""
        print(f"\n=== Rok {self.year} ===")
        print(f"Populacja: {len(self.humanity.humans)}")
        
        # Informacje o plemionach
        tribes = self.humanity.get_all_tribes()
        if tribes:
            print("\nPlemiona:")
            for i, tribe in enumerate(tribes, 1):
                print(f"  Plemię {i}: {tribe['leader'].name} (Członków: {len(tribe['members'])})")
        
        # Informacje o rodzinach
        families = sum(1 for h in self.humanity.humans 
                      if any(data.get("relation") == "spouse" 
                            for _, _, data in self.humanity.graph.edges(h, data=True))) / 2
        print(f"\nLiczba rodzin: {int(families)}")
        
        print("-" * 40)

    def initialize_population(self, initial_population: int):
        """Inicjalizacja z większą liczbą potencjalnych liderów"""
        for _ in range(initial_population):
            self.humanity.create_human()
            # Zwiększamy szansę na stworzenie potencjalnego lidera
            if random.random() < 0.3:  # 30% szans
                last_human = self.humanity.humans[-1]
                last_human.charisma = random.uniform(0.7, 1.0)
                last_human.courage = random.uniform(0.7, 1.0)
                last_human.intelligence = random.uniform(0.7, 1.0)
                last_human.age = random.randint(25, 40)  # Młodszy wiek dla potencjalnych liderów
        self.population_history.append(len(self.humanity.humans))
        
        
    def simulate_year(self):
        self.year += 1
        existing_tribes = self.humanity.get_all_tribes()
        
        # Naturalna śmierć ze zmniejszoną śmiertelnością
        to_remove = []
        for human in self.humanity.humans:
            human.age += 1
            death_chance = 0
            if human.age > 60:  # Zwiększamy próg śmiertelności
                death_chance = (human.age - 60) / 200  # Znacznie zmniejszona śmiertelność
            if random.random() < death_chance:
                to_remove.append(human)

        # Sprawdź czy usuwany człowiek jest liderem i znajdź zastępcę
        for human in to_remove:
            # Sprawdź czy jest liderem
            is_leader = any(data.get('relation') == 'leader' 
                        for _, _, data in self.humanity.graph.edges(human, data=True))
            
            if is_leader:
                # Znajdź plemię tego lidera
                for tribe in existing_tribes:
                    if tribe['leader'] == human:
                        # Znajdź nowego lidera wśród członków
                        potential_leaders = [
                            member for member in tribe['members']
                            if member.age >= self.humanity.LEADER_MIN_AGE
                            and member.charisma >= 0.6
                            and member not in to_remove
                        ]
                        
                        if potential_leaders:
                            # Wybierz nowego lidera
                            new_leader = max(potential_leaders,
                                        key=lambda h: h.charisma + h.courage + h.intelligence)
                            
                            # Usuń stare relacje lidera
                            edges_to_remove = []
                            for u, v, d in self.humanity.graph.edges(human, data=True):
                                if d.get('relation') in ['leader', 'member']:
                                    edges_to_remove.append((u, v))
                            
                            for edge in edges_to_remove:
                                self.humanity.graph.remove_edge(*edge)
                            
                            # Dodaj nowe relacje z nowym liderem
                            for member in tribe['members']:
                                if member != new_leader and member not in to_remove:
                                    self.humanity.graph.add_edge(new_leader, member, relation='leader')
                                    self.humanity.graph.add_edge(member, new_leader, relation='member')
                            
                            print(f"Nowy lider plemienia: {new_leader.name}")
                        break
        if len(self.humanity.get_all_tribes()) == 0:
            new_tribe = self.humanity.create_tribe()
        # Usuwanie zmarłych
        for human in to_remove:
            self.humanity.humans.remove(human)
            self.humanity.graph.remove_node(human)

        population = len(self.humanity.humans)
        if population >= self.humanity.MIN_TRIBE_SIZE:
            # Sprawdź liczbę istniejących plemion
            current_tribes = len(self.humanity.get_all_tribes())
            desired_tribes = max(1, population // 20)  # Jeden przywódca na każde 20 osób
            
            if current_tribes < desired_tribes:
                # Zwiększona liczba prób utworzenia plemienia
                for _ in range(5):  # 5 prób
                    new_tribe = self.humanity.create_tribe()


        # Tworzenie nowych rodzin z większą częstotliwością
        num_new_families = max(3, population // 6)  # Więcej rodzin
        for _ in range(num_new_families):
            self.humanity.create_family()

        self.population_history.append(population)

    def update_society_graph(self):
        self.ax_society.clear()
        G = self.humanity.graph
        
        if len(G.nodes()) == 0:
            self.ax_society.set_title("Brak ludzi w symulacji")
            return

        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Węzły
        node_colors = []
        node_sizes = []
        for human in G.nodes():
            if any(data.get('relation') == 'leader' for _, _, data in G.edges(human, data=True)):
                node_colors.append('#FF0000')
                node_sizes.append(1000)
            elif any(data.get('relation') == 'member' for _, _, data in G.edges(human, data=True)):
                node_colors.append('#4169E1')
                node_sizes.append(500)
            else:
                node_colors.append('#32CD32')
                node_sizes.append(300)

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                            node_size=node_sizes, ax=self.ax_society)

        # Krawędzie - poprawiona wersja
        edge_styles = {
            'leader': ('#FF0000', 'solid', 4),
            'member': ('#4169E1', 'dashed', 2),
            'spouse': ('#FF69B4', 'solid', 3),
            'father': ('#228B22', 'solid', 2),
            'mother': ('#9370DB', 'solid', 2)
        }

        for relation, (color, style, width) in edge_styles.items():
            edges = [(u, v) for (u, v, d) in G.edges(data=True) 
                    if d.get('relation') == relation]
            if edges:
                nx.draw_networkx_edges(G, pos, 
                                    edgelist=edges, 
                                    edge_color=color,
                                    style=style,
                                    width=width,
                                    ax=self.ax_society)

        # Etykiety
        labels = {human: f"{human.name}\n({human.age})" for human in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8, 
                            font_weight='bold', ax=self.ax_society)

        # Legenda
        legend_elements = [
            plt.Line2D([0], [0], color=color, linestyle=style,
                    label=relation.capitalize(), linewidth=width) 
            for relation, (color, style, width) in edge_styles.items()
        ]
        self.ax_society.legend(handles=legend_elements, loc='center left', 
                            bbox_to_anchor=(1, 0.5), fontsize=10)
        
        self.ax_society.set_title(f'Stan społeczeństwa - Rok {self.year}', 
                                fontsize=12, pad=20)
        self.ax_society.axis('off')
    def update_statistics(self):
        # Historia populacji
        self.ax1.clear()
        self.ax1.plot(range(len(self.population_history)), 
                     self.population_history, 'b-', linewidth=2)
        self.ax1.fill_between(range(len(self.population_history)), 
                            self.population_history, alpha=0.3)
        self.ax1.set_title('Historia populacji', fontsize=10)
        self.ax1.grid(True)
        
        # Statystyki plemion
        self.ax2.clear()
        tribes = self.humanity.get_all_tribes()
        
        if tribes:
            tribe_names = [f"P{i+1}" for i in range(len(tribes))]
            tribe_sizes = [len(tribe['members']) for tribe in tribes]
            strengths = [tribe['strength'] for tribe in tribes]
            wisdom = [tribe['wisdom'] for tribe in tribes]
            
            x = range(len(tribe_names))
            width = 0.25
            
            self.ax2.bar([i - width for i in x], tribe_sizes, width, 
                        label='Wielkość', color='green', alpha=0.7)
            self.ax2.bar([i for i in x], strengths, width, 
                        label='Siła', color='red', alpha=0.7)
            self.ax2.bar([i + width for i in x], wisdom, width, 
                        label='Mądrość', color='blue', alpha=0.7)
            
            self.ax2.set_xticks(x)
            self.ax2.set_xticklabels(tribe_names)
            self.ax2.set_title('Statystyki plemion', fontsize=10)
            self.ax2.legend(fontsize=8)
            self.ax2.grid(True, alpha=0.3)

        # Szczegółowe statystyki
        self.ax3.clear()
        population = len(self.humanity.humans)
        if population > 0:
            avg_age = sum(h.age for h in self.humanity.humans) / population
            num_families = sum(1 for h in self.humanity.humans 
                             if any(data.get("relation") == "spouse" 
                                   for _, _, data in self.humanity.graph.edges(h, data=True))) / 2
            
            stats_text = (
                f'Rok: {self.year}   |   '
                f'Populacja: {population}   |   '
                f'Plemiona: {len(tribes)}   |   '
                f'Średni wiek: {avg_age:.1f}   |   '
                f'Rodziny: {num_families:.0f}'
            )
            self.ax3.text(0.5, 0.5, stats_text, fontsize=12, 
                         ha='center', va='center')
            self.ax3.axis('off')

    def run_simulation_step(self):
        """Wykonuje jeden rok symulacji"""
        self.simulate_year()
        self.update_society_graph()
        self.update_statistics()
        self.fig.tight_layout()
        plt.draw()
        
    def on_close(self, event):
        """Obsługa zamknięcia okna"""
        plt.close('all')

if __name__ == "__main__":
    sim = Simulation()
    sim.initialize_population(50)
    sim.run()  # Zamiast plt.show()
    
    
    
