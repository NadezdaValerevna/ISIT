"""Модуль обработки действий правил."""


class ActionHandler:
    """Обработчик действий правил."""

    def __init__(self, memory):
        self.memory = memory

    def execute(self, action: dict):
        """Выполняет действие в зависимости от типа."""
        atype = action['type']

        if atype == 'assert':
            self.memory.facts[action['fact']] = action['value']
            print(f"  [Факт: {action['fact']} = {action['value']}]")

        elif atype == 'ask_user':
            qid = action['question']
            fact_name = action['fact']
            if qid not in self.memory.asked:
                ans = self.memory.ask_question(qid)
                self.memory.facts[fact_name] = ans
                self.memory.asked.add(qid)
                print(f"  [Ответ: {fact_name} = {ans}]")

        elif atype == 'calculate_mbti_type':
            self._calculate_mbti()

        elif atype == 'generate_personality_report':
            self._generate_report()

        elif atype == 'generate_career_recommendations':
            self._generate_career_recommendations()

        elif atype == 'generate_communication_recommendations':
            self._generate_communication_recommendations()

        elif atype == 'generate_growth_recommendations':
            self._generate_growth_recommendations()

    def _calculate_mbti(self):
        """Вычисляет тип MBTI."""
        e = 'E' if self.memory.facts.get('energy_source') == 'extraversion' else 'I'
        s = 'S' if self.memory.facts.get('information_processing') == 'sensing' else 'N'
        t = 'T' if self.memory.facts.get('decision_making') == 'thinking' else 'F'
        j = 'J' if self.memory.facts.get('lifestyle') == 'judging' else 'P'

        mbti = e + s + t + j
        self.memory.facts['mbti_type'] = mbti
        print(f"  [Рассчитан тип MBTI: {mbti}]")

    def _generate_report(self):
        """Генерирует отчет личности."""
        parts = []

        if 'mbti_type' in self.memory.facts:
            parts.append(f"Тип личности: {self.memory.facts['mbti_type']}")

        if 'diagnosis' in self.memory.facts:
            parts.append(f"Описание: {self.memory.facts['diagnosis']}")

        big5 = []
        for key, label in [
            ('extraversion_analysis', 'Экстраверсия'),
            ('openness_analysis', 'Открытость'),
            ('conscientiousness_analysis', 'Добросовестность'),
            ('emotional_analysis', 'Эмоциональность')
        ]:
            if key in self.memory.facts:
                big5.append(f"{label}: {self.memory.facts[key]}")

        if big5:
            parts.append("Черты личности:")
            parts.extend([f"  - {item}" for item in big5])

        self.memory.facts['integrated_report'] = "\n".join(parts)
        print("  [Создан отчет]")

    def _generate_career_recommendations(self):
        """Генерирует карьерные рекомендации."""
        mbti = self.memory.facts.get('mbti_type')
        if mbti:
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
            self.memory.facts['career_recommendation'] = rec
            print(f"  [Созданы карьерные рекомендации]")

    def _generate_communication_recommendations(self):
        """Генерирует рекомендации по общению."""
        e_type = self.memory.facts.get('personality_category')
        p_type = self.memory.facts.get('perception_category')

        if e_type == 'extrovert':
            comm = 'Вы экстраверт: предпочитаете устное общение, работаете в команде'
        else:
            comm = 'Вы интроверт: предпочитаете письменное общение, работаете в уединении'

        if p_type == 'sensor':
            comm += '. Ориентируетесь на факты и конкретику в общении.'
        else:
            comm += '. Ориентируетесь на идеи и общую картину в общении.'

        self.memory.facts['communication_recommendation'] = comm
        print("  [Созданы рекомендации по общению]")

    def _generate_growth_recommendations(self):
        """Генерирует рекомендации для роста."""
        mbti = self.memory.facts.get('mbti_type', '')
        stability = self.memory.facts.get('emotional_stability', 3)

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

        self.memory.facts['growth_recommendation'] = '; '.join(rec) if rec else 'Развивайте сильные стороны вашего типа'
        print("  [Созданы рекомендации для роста]")