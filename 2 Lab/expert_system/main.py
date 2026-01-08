"""Точка входа в программу."""

from engine import RuleEngine


def main():
    try:
        engine = RuleEngine('lab.json')
        engine.run()

        while True:
            again = input("\nНовый анализ? (да/нет): ").lower()
            if again in ['да', 'д', 'yes', 'y']:
                print("\n" + "=" * 50)
                engine = RuleEngine('lab.json')
                engine.run()
            else:
                print("\nДо свидания!")
                break

    except FileNotFoundError:
        print("Файл lab.json не найден")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()