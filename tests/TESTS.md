# Symulacja społeczeństwa

Ten kod przedstawia symulację społeczeństwa, w której tworzone są osoby, tworzone są relacje między nimi, a ich cechy wpływają na ich zachowanie i interakcje. Symulacja jest wyświetlana w interaktywnym oknie.

## Użycie

Aby uruchomić symulację, należy uruchomić skrypt `main.py`. Możesz dostosować parametry symulacji, takie jak początkowa populacja, poprzez edycję metody `initialize_population` w klasie `Simulation`.

## Przykład użycia

```python
if __name__ == "__main__":
    sim = Simulation()
    sim.initialize_population(50)  # Ustawienie początkowej populacji na 50 osób
    sim.run()  # Uruchomienie symulacji
```

## Wyniki

Symulacja wyświetla stan społeczeństwa w postaci grafu, który pokazuje relacje między osobami. W oknie znajdują się również wykresy przedstawiające historię populacji, statystyki plemion, oraz szczegółowe statystyki symulacji.

Symulacja pozwala na obserwację zachowania społeczeństwa w zależności od parametrów, takich jak początkowa populacja, wielkość plemion, siła i mądrość liderów, itp.

## Dalsze kroki

Możesz dalej rozwijać ten projekt, dodając nowe funkcjonalności, modyfikując istniejące, lub poprawiając wydajność symulacji. Możesz również eksperymentować z różnymi algorytmami tworzenia relacji między osobami, lub zmieniać sposób, w jaki osoby wpływają na siebie.

## Zrzuty ekranu

Poniżej przedstawiono kilka zrzutów ekranu z działającej symulacji:

![map generator](./tests/01.png)

![cywilization](./tests/02.png)

