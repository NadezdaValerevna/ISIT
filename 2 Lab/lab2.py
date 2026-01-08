import json
from typing import Any, Dict, List
class RuleEngine:
    def __init__(self, rules_file: str = 'lab.json'):
        with open(rules_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.rules = data['rules']
        self.questions = data['questions']
        self.facts = data['initial_facts'].copy()
        self.asked = set()

        # Для MBTI
        self.mbti_map = data.get('mbti_mapping', {})

    def ask(self, qid: str) -> Any:
        q = self.questions[qid]
        print(f"\n{q['text']}")

        if 'explanation' in q:
            print(f"({q['explanation']})")

        if q['type'] == 'boolean':
            while True:
                ans = input("(да/нет): ").lower()
                if ans in ['да', 'д', 'yes', 'y', '1']:
                    return True
                elif ans in ['нет', 'н', 'no', 'n', '0']:
                    return False

        elif q['type'] == 'integer':
            while True:
                try:
                    val = int(input("Введите число: "))
                    if 'validation' in q:
                        if q['validation'] == 'min_0' and val < 0:
                            print("Должно быть >= 0")
                            continue
                        if q['validation'] == 'range_1_5' and not (1 <= val <= 5):
                            print("Должно быть от 1 до 5")
                            continue
                    return val
                except:
                    print("Введите целое число")

        elif q['type'] == 'choice':
            print(f"Варианты: {', '.join(q['options'])}")
            while True:
                ans = input("Ваш выбор: ")
                if ans in q['options']:
                    return ans

    def check_condition(self, cond: Dict) -> bool:
        fact = self.facts.get(cond['fact'])

        if 'exists' in cond:
            return (fact is not None) if cond['exists'] else (fact is None)

        if fact is None:
            return False

        if 'operator' not in cond:
            expected = cond['value']
            if isinstance(expected, list):
                return fact in expected
            return fact == expected

        op = cond['operator']
        expected = cond['value']

        if op == '>': return fact > expected
        if op == '>=': return fact >= expected
        if op == '<': return fact < expected
        if op == '<=': return fact <= expected
        return False

    def check_all(self, conditions: List[Dict]) -> bool:
        return all(self.check_condition(c) for c in conditions)

    def execute_action(self, action: Dict):
        atype = action['type']

        if atype == 'assert':
            self.facts[action['fact']] = action['value']
            print(f"  [Факт: {action['fact']} = {action['value']}]")

        elif atype == 'ask_user':
            qid = action['question']
            fact_name = action['fact']
            if qid not in self.asked:
                ans = self.ask(qid)
                self.facts[fact_name] = ans
                self.asked.add(qid)
                print(f"  [Ответ: {fact_name} = {ans}]")

        elif atype == 'calculate_mbti_type':
            # Преобразуем ответы в буквы MBTI
            e = 'E' if self.facts.get('energy_source') == 'extraversion' else 'I'
            s = 'S' if self.facts.get('information_processing') == 'sensing' else 'N'
            t = 'T' if self.facts.get('decision_making') == 'thinking' else 'F'
            j = 'J' if self.facts.get('lifestyle') == 'judging' else 'P'

            mbti = e + s + t + j
            self.facts['mbti_type'] = mbti
            print(f"  [Рассчитан тип MBTI: {mbti}]")

        elif atype == 'generate_personality_report':
            # Собираем отчет
            parts = []

            if 'mbti_type' in self.facts:
                parts.append(f"Тип личности: {self.facts['mbti_type']}")

            if 'diagnosis' in self.facts:
                parts.append(f"Описание: {self.facts['diagnosis']}")

            # Добавляем анализ Big Five
            big5 = []
            for key, label in [
                ('extraversion_analysis', 'Экстраверсия'),
                ('openness_analysis', 'Открытость'),
                ('conscientiousness_analysis', 'Добросовестность'),
                ('emotional_analysis', 'Эмоциональность')
            ]:
                if key in self.facts:
                    big5.append(f"{label}: {self.facts[key]}")

            if big5:
                parts.append("Черты личности:")
                parts.extend([f"  - {item}" for item in big5])

            self.facts['integrated_report'] = "\n".join(parts)
            print("  [Создан отчет]")

        elif atype == 'generate_career_recommendations':
            mbti = self.facts.get('mbti_type')
            if mbti:
                # Простые рекомендации по типу
                recommendations = {
                    'INTJ': 'Научные исследования, IT-архитектура, стратегическое планирование',
                    'INFJ': 'Психология, коучинг, социальная работа',
                    'ENTP': 'Предпринимательство, маркетинг, консалтинг',
                    'ENFJ': 'Обучение, управление, общественная деятельность',
                    'ISTJ': 'Бухгалтерия, администрирование, логистика',
                    'ISFP': 'Дизайн, искусство, музыка',
                    'ESTP': 'Продажи, спорт, мероприятия',
                    'ESFJ': 'Медицина, образование, уход за людьми',
                    'ISTP': 'Технические специальности, механика',
                    'ISFJ': 'Медицина, библиотечное дело, архивирование',
                    'INTP': 'Программирование, научная работа',
                    'INFP': 'Психология, писательство, искусство',
                    'ENTJ': 'Менеджмент, политика, юриспруденция',
                    'ENFP': 'Маркетинг, PR, творческие профессии',
                    'ESTJ': 'Управление, организация, контроль',
                    'ESFP': 'Развлечения, туризм, сервис'
                }

                rec = recommendations.get(mbti, 'Разнообразные профессии, подходящие вашему типу личности')
                self.facts['career_recommendation'] = rec
                print(f"  [Созданы карьерные рекомендации]")

        elif atype == 'generate_communication_recommendations':
            e_type = self.facts.get('personality_category')
            p_type = self.facts.get('perception_category')

            if e_type == 'extrovert':
                comm = 'Вы экстраверт: предпочитаете устное общение, работаете в команде'
            else:
                comm = 'Вы интроверт: предпочитаете письменное общение, работаете в уединении'

            if p_type == 'sensor':
                comm += '. Ориентируетесь на факты и конкретику в общении.'
            else:
                comm += '. Ориентируетесь на идеи и общую картину в общении.'

            self.facts['communication_recommendation'] = comm
            print("  [Созданы рекомендации по общению]")

        elif atype == 'generate_growth_recommendations':
            mbti = self.facts.get('mbti_type', '')
            stability = self.facts.get('emotional_stability', 3)

            rec = []

            if 'I' in mbti:
                rec.append('Развивайте социальные навыки')
            if 'E' in mbti:
                rec.append('Учитесь слушать и анализировать')
            if 'T' in mbti:
                rec.append('Развивайте эмпатию')
            if 'F' in mbti:
                rec.append('Учитесь объективности')

            if stability < 3:
                rec.append('Работайте над эмоциональной устойчивостью')

            self.facts['growth_recommendation'] = '; '.join(rec) if rec else 'Развивайте сильные стороны вашего типа'
            print("  [Созданы рекомендации для роста]")

    def run_cycle(self) -> bool:
        activated = []
        for rule in self.rules:
            if self.check_all(rule['conditions']):
                activated.append(rule)

        if not activated:
            return False

        for rule in activated:
            for action in rule['actions']:
                self.execute_action(action)

        return True

    def run(self):
        print("\n" + "=" * 50)
        print("Экспертная система: Анализ личности")
        print("=" * 50)

        cycle = 0
        while cycle < 50:
            cycle += 1

            # Проверяем, все ли данные собраны
            if self.facts.get('all_data_collected'):
                # Запускаем еще несколько циклов для обработки рекомендаций
                for _ in range(5):
                    self.run_cycle()
                break

            if not self.run_cycle():
                # Прямой опрос
                for rule in self.rules:
                    for action in rule.get('actions', []):
                        if action['type'] == 'ask_user':
                            qid = action['question']
                            fact = action['fact']
                            if qid not in self.asked and self.facts.get(fact) is None:
                                ans = self.ask(qid)
                                self.facts[fact] = ans
                                self.asked.add(qid)
                                break
                    else:
                        continue
                    break
                else:
                    # Больше нет вопросов
                    break

        # Вывод результатов
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ АНАЛИЗА")
        print("=" * 50)

        if 'mbti_type' in self.facts:
            print(f"\n ТИП ЛИЧНОСТИ: {self.facts['mbti_type']}")

        if 'diagnosis' in self.facts:
            print(f"\n ОПИСАНИЕ:\n{self.facts['diagnosis']}")

        # Анализ Big Five
        big5_found = False
        for key, label in [
            ('extraversion_analysis', 'Экстраверсия'),
            ('openness_analysis', 'Открытость'),
            ('conscientiousness_analysis', 'Добросовестность'),
            ('emotional_analysis', 'Эмоциональная стабильность')
        ]:
            if key in self.facts:
                if not big5_found:
                    print(f"\n ЧЕРТЫ ЛИЧНОСТИ:")
                    big5_found = True
                print(f"  • {label}: {self.facts[key]}")

        # Рекомендации
        if 'career_recommendation' in self.facts:
            print(f"\n КАРЬЕРА:\n{self.facts['career_recommendation']}")

        if 'communication_recommendation' in self.facts:
            print(f"\n  ОБЩЕНИЕ:\n{self.facts['communication_recommendation']}")

        if 'growth_recommendation' in self.facts:
            print(f"\n РАЗВИТИЕ:\n{self.facts['growth_recommendation']}")

        if 'integrated_report' in self.facts:
            print(f"\n ПОЛНЫЙ ОТЧЕТ:\n{self.facts['integrated_report']}")


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