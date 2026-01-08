"""
Пользовательский интерфейс
"""

class Interface:
    """Текстовый интерфейс"""

    def __init__(self, engine):
        self.engine = engine

    def display_welcome(self):
        """Показывает приветствие"""
        print("\n" + "="*50)
        print("   СИСТЕМА ОПРЕДЕЛЕНИЯ АРХЕТИПОВ ЛИЧНОСТИ")
        print("="*50)
        print("Отвечайте 'yes' или 'no' на вопросы")
        print("="*50 + "\n")

    def ask_question(self, question_node):
        """Задает вопрос"""
        print(f"Вопрос: {question_node.attrs['text']}")
        while True:
            answer = input("Ваш ответ (yes/no): ").strip().lower()
            if answer in ["yes", "no", "y", "n", "да", "нет"]:
                # Нормализуем ответ
                if answer in ["yes", "y", "да"]:
                    return "yes"
                else:
                    return "no"
            print("Пожалуйста, ответьте 'yes' или 'no'")

    def display_reasoning_chain(self):
        """Показывает цепочку рассуждений"""
        chain = self.engine.memory.get_reasoning_chain()
        if chain:
            print("\n" + "="*50)
            print("   ЦЕПОЧКА РАССУЖДЕНИЙ:")
            print("="*50)
            for i, step in enumerate(chain, 1):
                print(f"{i}. {step}")

    def display_detailed_facts(self):
        """Показывает детализированные факты"""
        facts = self.engine.memory.get_all_facts()
        if facts:
            print("\n" + "-"*50)
            print("ДЕТАЛИЗИРОВАННЫЕ ОТВЕТЫ:")
            print("-"*50)
            for var, val in facts.items():
                print(f"  • {var}: {val}")

    def display_result(self, archetype):
        """Показывает результат с обоснованием"""
        if archetype:
            node = self.engine.network.get_node(archetype)
            if node:
                print("\n" + "="*50)
                print(f"   ВАШ АРХЕТИП: {archetype}")
                print("="*50)
                print(f"Описание: {node.attrs['desc']}")
                print(f"\nОбоснование: {node.attrs['reason']}")
                print("="*50)
        else:
            print("\nНедостаточно данных для определения архетипа")

    def display_final_summary(self, archetype):
        """Показывает итоговую сводку"""
        self.display_result(archetype)
        self.display_reasoning_chain()
        self.display_detailed_facts()

        # Показываем путь принятия решений
        print("\n" + "="*50)
        print("   ПУТЬ ПРИНЯТИЯ РЕШЕНИЙ:")
        print("="*50)

        facts = self.engine.memory.get_all_facts()

        if "justice" in facts:
            if facts["justice"] == "yes":
                print("1. Ветвь: Справедливость (принципы важнее гармонии)")
                if "planning" in facts:
                    if facts["planning"] == "yes":
                        print("2. Подход: Планирование (планируете перед действием)")
                        if "detail" in facts:
                            print(f"3. Стиль: {'Детализация' if facts['detail'] == 'yes' else 'Общая картина'}")
                    else:
                        print("2. Подход: Действие (действуете немедленно)")
                        if "leader" in facts:
                            print(f"3. Стиль: {'Лидерство' if facts['leader'] == 'yes' else 'Исполнение'}")
            else:
                print("1. Ветвь: Гармония (гармония важнее принципов)")
                if "cooperation" in facts:
                    if facts["cooperation"] == "yes":
                        print("2. Подход: Сотрудничество (работаете с другими)")
                        if "empathy" in facts:
                            print(f"3. Стиль: {'Эмпатия' if facts['empathy'] == 'yes' else 'Дипломатия'}")
                    else:
                        print("2. Подход: Творчество (ищете нестандартные решения)")
                        if "imagination" in facts:
                            print(f"3. Стиль: {'Воображение' if facts['imagination'] == 'yes' else 'Интуиция'}")

        # Сводка по ответам
        print("\n" + "-"*50)
        print("СВОДКА ОТВЕТОВ:")
        print("-"*50)

        answer_descriptions = {
            "justice": {
                "yes": "Приоритет справедливости",
                "no": "Приоритет гармонии"
            },
            "planning": {
                "yes": "Предпочитает планирование",
                "no": "Предпочитает действие"
            },
            "cooperation": {
                "yes": "Предпочитает сотрудничество",
                "no": "Предпочитает творчество"
            },
            "detail": {
                "yes": "Ориентирован на детали",
                "no": "Видит общую картину"
            },
            "leader": {
                "yes": "Природный лидер",
                "no": "Целеустремленный исполнитель"
            },
            "empathy": {
                "yes": "Глубокая эмпатия",
                "no": "Дипломатические навыки"
            },
            "imagination": {
                "yes": "Богатое воображение",
                "no": "Сильная интуиция"
            }
        }

        for var, val in facts.items():
            desc = answer_descriptions.get(var, {}).get(val, "")
            if desc:
                print(f"  • {desc}")

    def run(self):
        """Запускает диалог"""
        self.display_welcome()

        while True:
            # Получаем следующий вопрос
            next_q = self.engine.infer_next_question()

            if not next_q:
                # Нет вопросов - пробуем определить результат
                result = self.engine.infer_archetype()
                self.display_final_summary(result)
                break

            # Задаем вопрос
            answer = self.ask_question(next_q)

            # Обрабатываем ответ
            result = self.engine.process_answer(next_q, answer)

            # Если сразу получили результат
            if result:
                self.display_final_summary(result)
                break

        # Предложение начать заново
        print("\n" + "-"*50)
        restart = input("Начать заново? (yes/no): ").strip().lower()
        if restart in ["yes", "y", "да"]:
            self.engine.memory.clear()
            print("\n"*2)
            self.run()
        else:
            print("\nСпасибо за использование системы!")