// Translations for Finance App
// Supported languages: Uzbek (uz), Russian (ru), English (en)

const translations = {
    uz: {
        // App & Navigation
        'app_name': 'Finance App',
        'dashboard': 'Bosh sahifa',
        'wallets': 'Hamyonlar',
        'categories': 'Kategoriyalar',
        'transactions': 'Tranzaksiyalar',
        'transfers': "O'tkazmalar",
        'statistics': 'Statistika',
        'chat': 'Chat',
        'profile': 'Profil',
        'admin_panel': 'Admin Panel',
        'admin_dashboard': 'Admin Dashboard',
        'messages': 'Xabarlar',
        'admin_with': 'Admin bilan',
        'go_to_django_admin': 'Django Admin Panelga o\'tish',
        'latest_message': 'So\'nggi xabar',
        'waiting_reply': 'Javob kutilmoqda',
        'replied': 'Javob berilgan',
        'logout': 'Chiqish',
        'login': 'Kirish',
        'register': "Ro'yxatdan o'tish",

        // Common Actions
        'add': "Qo'shish",
        'create': 'Yaratish',
        'edit': 'Tahrirlash',
        'update': 'Yangilash',
        'delete': "O'chirish",
        'save': 'Saqlash',
        'cancel': 'Bekor qilish',
        'filter': 'Filtrlash',
        'search': 'Qidirish',
        'view': "Ko'rish",
        'back': 'Orqaga',
        'next': 'Keyingi',
        'submit': 'Yuborish',
        'close': 'Yopish',
        'view_all': 'Barchasi',
        'quick_actions': 'Tezkor amallar',

        // Wallet related
        'wallet': 'Hamyon',
        'wallet_list': 'Hamyonlar ro\'yxati',
        'add_wallet': 'Hamyon qo\'shish',
        'wallet_type': 'Hamyon turi',
        'cash': 'Naqd',
        'card': 'Karta',
        'card_number': 'Karta raqami',
        'card_type': 'Karta turi',
        'humo': 'Humo',
        'uzcard': 'UzCard',
        'visa': 'Visa',
        'mastercard': 'MasterCard',
        'balance': 'Balans',
        'total_balance': 'Umumiy balans',
        'wallets_balance': 'Hamyonlar balansi',
        'currency': 'Valyuta',
        'title': 'Nomi',
        'no_wallets': 'Hamyonlar yo\'q',

        // Category related
        'category': 'Kategoriya',
        'category_list': 'Kategoriyalar ro\'yxati',
        'add_category': 'Kategoriya qo\'shish',
        'category_name': 'Kategoriya nomi',
        'category_type': 'Kategoriya turi',
        'income': 'Kirim',
        'expense': 'Chiqim',
        'icon': 'Ikonka',

        // Transaction related
        'transaction': 'Tranzaksiya',
        'transaction_list': 'Tranzaksiyalar ro\'yxati',
        'recent_transactions': 'So\'nggi tranzaksiyalar',
        'transaction_history': 'Tranzaksiyalar tarixi',
        'add_income': 'Kirim qo\'shish',
        'add_expense': 'Chiqim qo\'shish',
        'daily_income': 'Kunlik kirim',
        'daily_expense': 'Kunlik chiqim',
        'total_income': 'Umumiy kirim',
        'total_expense': 'Umumiy chiqim',
        'amount': 'Miqdor',
        'description': 'Izoh',
        'date': 'Sana',
        'exchange_rate': 'Kurs',
        'no_income': 'Kirim yo\'q',
        'no_expense': 'Chiqim yo\'q',

        // Transfer related
        'transfer': "O'tkazma",
        'transfer_list': "O'tkazmalar ro'yxati",
        'add_transfer': "O'tkazma qo'shish",
        'from_wallet': 'Qaysi hamyondan',
        'to_wallet': 'Qaysi hamyonga',

        // Statistics
        'by_period_filter': 'Davr bo\'yicha filter',
        'select_period': 'Davr tanlang',
        'period': 'Davr',
        'daily': 'Kunlik',
        'weekly': 'Haftalik',
        'monthly': 'Oylik',
        'yearly': 'Yillik',
        'custom': 'Belgilangan muddat',

        // Months
        'january': 'Yanvar',
        'february': 'Fevral',
        'march': 'Mart',
        'april': 'Aprel',
        'may': 'May',
        'june': 'Iyun',
        'july': 'Iyul',
        'august': 'Avgust',
        'september': 'Sentabr',
        'october': 'Oktabr',
        'november': 'Noyabr',
        'december': 'Dekabr',
        'custom': 'Belgilangan muddat',
        'start_date': 'Boshlanish sanasi',
        'end_date': 'Tugash sanasi',
        'period_range': 'davr',
        'from': 'dan',
        'to': 'gacha',
        'total_income': 'Jami kirim',
        'total_expense': 'Jami chiqim',
        'created_at_text': 'da yaratilgan',
        'income_by_category': 'Kategoriyalar bo\'yicha kirimlar',
        'expense_by_category': 'Kategoriyalar bo\'yicha chiqimlar',
        'day': 'Kun',
        'month': 'Oy',
        'year': 'Yil',
        'select_day': '--- Kun tanlang ---',
        'select_month': '--- Oy tanlang ---',
        'select_year': '--- Yil tanlang ---',
        'no_income_data': 'Kirimlar mavjud emas',
        'no_expense_data': 'Chiqimlar mavjud emas',

        // Months
        'january': 'Yanvar',
        'february': 'Fevral',
        'march': 'Mart',
        'april': 'Aprel',
        'may': 'May',
        'june': 'Iyun',
        'july': 'Iyul',
        'august': 'Avgust',
        'september': 'Sentabr',
        'october': 'Oktabr',
        'november': 'Noyabr',
        'december': 'Dekabr',

        // Auth
        'phone_number': 'Telefon raqam',
        'password': 'Parol',
        'confirm_password': 'Parolni tasdiqlang',
        'first_name': 'Ism',
        'last_name': 'Familiya',
        'username': 'Username',
        'username_help': 'Agar kiritmasangiz, avtomatik yaratiladi',
        'password_help': 'Agar kiritmasangiz, avtomatik yaratiladi',
        'finish_registration': 'Ro\'yxatdan o\'tishni yakunlash',
        'otp_header': 'Tasdiqlash kodi',
        'otp_help': 'Telefoningizga yuborilgan kodni kiriting',
        'otp_sent_to': 'raqamiga kod yuborildi',
        'code_6_digits': '6-xonali kod',
        'resend_otp': 'Kodni qayta yuborish',
        'complete_registration_details': 'Qo\'shimcha ma\'lumotlarni kiriting (ixtiyoriy)',
        'forgot_password': 'Parolni unutdingizmi?',
        'remember_me': 'Eslab qolish',

        // Profile
        'personal_info': 'Shaxsiy ma\'lumotlar',
        'changeable': 'O\'zgartirish mumkin',
        'phone_not_changeable': 'Telefon raqamni o\'zgartirib bo\'lmaydi',
        'change_password': 'Parolni o\'zgartirish',
        'current_password': 'Joriy parol',
        'new_password': 'New Password:',
        'confirm_new_password': 'Confirm New Password:',
        'current_password_help': 'Parolni o\'zgartirish uchun joriy parolni kiriting',
        'profile_stats': 'Profil statistikasi',
        'registration_date': 'Ro\'yxatdan o\'tgan sana',
        'account_status': 'Hisob holati',
        'last_activity': 'So\'nggi faollik',
        'required': 'Kerak',
        'available': 'Bor',

        // Transfers
        'sent': 'Yuborilgan',
        'received': 'Qabul qilingan',
        'create_transfer': 'O\'tkazma yaratish',
        'transfer_info': 'O\'tkazma ma\'lumotlari',
        'receiver': 'Qabul qiluvchi',
        'make_transfer': 'O\'tkazmani amalga oshirish',
        'transfer_details': 'O\'tkazma tafsilotlari',
        'sent_amount': 'Yuborilgan summa',
        'received_amount': 'Qabul qilingan summa',

        // Messages
        'no_data': 'Ma\'lumot yo\'q',
        'loading': 'Yuklanmoqda...',
        'success': 'Muvaffaqiyatli',
        'error': 'Xatolik',
        'confirm_delete': 'Rostdan ham o\'chirmoqchimisiz?',
        'are_you_sure': 'Ishonchingiz komilmi?',

        // Wallet Forms
        'create_wallet': 'Yangi hamyon yaratish',
        'edit_wallet': 'Hamyonni tahrirlash',
        'delete_wallet': 'Hamyonni o\'chirish',
        'wallet_info': 'Hamyon ma\'lumotlari',
        'initial_balance': 'Boshlang\'ich balans',
        'initial_balance_help': 'Agar mablag\' qo\'shmoqchi bo\'lsangiz, miqdorni kiriting',
        'card_name_example': 'Masalan: "Humo kartam"',
        'wallet_not_found': 'Hamyon topilmadi',
        'wallet_name': 'Hamyon nomi',

        // Category Forms
        'create_category': 'Yangi kategoriya yaratish',
        'edit_category': 'Kategoriyani tahrirlash',
        'delete_category': 'Kategoriyani o\'chirish',
        'category_info': 'Kategoriya ma\'lumotlari',
        'category_name_help': 'Masalan: "Oylik maosh", "Oziq-ovqat"',
        'category_warning': 'Diqqat! Bu kategoriyaga tegishli barcha tranzaksiyalar o\'chiriladi.',
        'created_at': 'Yaratilgan sana',

        // Transaction Forms
        'new_income': 'Yangi Kirim',
        'new_expense': 'Yangi Chiqim',
        'delete_transaction': 'Tranzaksiyani o\'chirish',
        'wallet_not_found_create_one': 'Hamyon mavjud emas. Avval hamyon yaratib oling.',
        'description_help': 'Izoh qoldiring (ixtiyoriy)',
        'balance_check': 'Balans tekshirish',
        'converted_amount': 'Konvert qilingan miqdor',
        'sufficient_funds': 'Yetarli',
        'insufficient_funds': 'Yetarli emas',
        'amount_required': 'Miqdor kiritilishi shart',
        'wallet_balance_will_decrease': 'Hamyon balansi kamayadi',
        'wallet_balance_will_increase': 'Hamyon balansi ko\'payadi',
        'attention': 'Diqqat!',
        'wallet_info': 'Hamyon ma\'lumotlari',
        'transaction_info': 'Tranzaksiya ma\'lumotlari',

        // Chat
        'chat_list': 'Chatlar ro\'yxati',
        'chat_user': 'Foydalanuvchi',
        'status': 'Holat',
        'actions': 'Harakat',
        'me': 'Men',
        'ago': 'oldin',
        'oldin': 'oldin', // Duplicate for fallback
        'new_messages_count': 'yangi',
        'closed': 'Yopilgan',
        'open': 'Ochish',
        'no_messages': 'Xabarlar yo\'q',
        'start_chat_with_users': 'Foydalanuvchilar bilan suhbatni boshlang',
        'start_chat_with_user': 'Foydalanuvchi bilan suhbatni boshlang',
        'user_info': 'Foydalanuvchi ma\'lumotlari',
        'user_status': 'Holati',
        'wallets_count': 'Hamyonlar soni',
        'open_in_admin_panel': 'Admin panelda ochish',
        'admin_name': 'Admin',
        'online': 'Online',
        'offline': 'Offline',
        'start_chat_with_admin': 'Admin bilan suhbatni boshlang',
        'chat_info': 'Chat ma\'lumotlari',
        'help_center': 'Yordam markazi',
        'messages_count': 'Xabarlar soni',
        'admin_reply_time_help': 'Admin javobi odatda 24 soat ichida keladi',
        'placeholder_message': 'Xabar yozing...',
    },

    ru: {
        // App & Navigation
        'app_name': 'Finance App',
        'dashboard': 'Главная',
        'wallets': 'Кошельки',
        'categories': 'Категории',
        'transactions': 'Транзакции',
        'transfers': 'Переводы',
        'statistics': 'Статистика',
        'chat': 'Чат',
        'profile': 'Профиль',
        'admin_panel': 'Админ Панель',
        'chat_admin': 'Админ Чат',
        'admin_dashboard': 'Панель администратора',
        'messages': 'Сообщения',
        'admin_with': 'с Админом',
        'logout': 'Выход',
        'login': 'Вход',
        'register': 'Регистрация',

        // Common Actions
        'add': 'Добавить',
        'create': 'Создать',
        'edit': 'Редактировать',
        'update': 'Обновить',
        'delete': 'Удалить',
        'save': 'Сохранить',
        'cancel': 'Отмена',
        'filter': 'Фильтровать',
        'search': 'Поиск',
        'view': 'Просмотр',
        'back': 'Назад',
        'next': 'Далее',
        'submit': 'Отправить',
        'close': 'Закрыть',
        'view_all': 'Все',
        'quick_actions': 'Быстрые действия',

        // Wallet related
        'wallet': 'Кошелек',
        'wallet_list': 'Список кошельков',
        'add_wallet': 'Добавить кошелек',
        'wallet_type': 'Тип кошелька',
        'cash': 'Наличные',
        'card': 'Карта',
        'card_number': 'Номер карты',
        'card_type': 'Тип карты',
        'humo': 'Humo',
        'uzcard': 'UzCard',
        'visa': 'Visa',
        'mastercard': 'MasterCard',
        'balance': 'Баланс',
        'total_balance': 'Общий баланс',
        'wallets_balance': 'Баланс кошельков',
        'currency': 'Валюта',
        'title': 'Название',
        'no_wallets': 'Кошельков нет',

        // Category related
        'category': 'Категория',
        'category_list': 'Список категорий',
        'add_category': 'Добавить категорию',
        'category_name': 'Название категории',
        'category_type': 'Тип категории',
        'income': 'Доход',
        'expense': 'Расход',
        'icon': 'Иконка',

        // Transaction related
        'transaction': 'Транзакция',
        'transaction_list': 'Список транзакций',
        'recent_transactions': 'Последние транзакции',
        'transaction_history': 'История транзакций',
        'add_income': 'Добавить доход',
        'add_expense': 'Добавить расход',
        'daily_income': 'Дневной доход',
        'daily_expense': 'Дневной расход',
        'total_income': 'Общий доход',
        'total_expense': 'Общий расход',
        'amount': 'Сумма',
        'description': 'Описание',
        'date': 'Дата',
        'exchange_rate': 'Курс',
        'no_income': 'Доходов нет',
        'no_expense': 'Расходов нет',

        // Transfer related
        'transfer': 'Перевод',
        'transfer_list': 'Список переводов',
        'add_transfer': 'Добавить перевод',
        'from_wallet': 'Из кошелька',
        'to_wallet': 'В кошелек',

        // Statistics
        'by_period_filter': 'Фильтр по периоду',
        'select_period': 'Выберите период',
        'period': 'Период',
        'daily': 'Ежедневно',
        'weekly': 'Еженедельно',
        'monthly': 'Ежемесячно',
        'yearly': 'Ежегодно',
        'custom': 'Указанный период',

        // Months
        'january': 'Январь',
        'february': 'Февраль',
        'march': 'Март',
        'april': 'Апрель',
        'may': 'Май',
        'june': 'Июнь',
        'july': 'Июль',
        'august': 'Август',
        'september': 'Сентябрь',
        'october': 'Октябрь',
        'november': 'Ноябрь',
        'december': 'Декабрь',
        'custom_range': 'Пользовательский',
        'start_date': 'Дата начала',
        'end_date': 'Дата окончания',
        'period_range': 'период',
        'from': 'с',
        'to': 'по',
        'total_income': 'Общий доход',
        'total_expense': 'Общий расход',
        'income_by_category': 'Доходы по категориям',
        'expense_by_category': 'Расходы по категориям',
        'day': 'День',
        'month': 'Месяц',
        'year': 'Год',
        'select_day': '--- Выберите день ---',
        'select_month': '--- Выберите месяц ---',
        'select_year': '--- Выберите год ---',
        'no_income_data': 'Доходы отсутствуют',
        'no_expense_data': 'Расходы отсутствуют',

        // Auth
        'phone_number': 'Номер телефона',
        'password': 'Пароль',
        'confirm_password': 'Подтвердите пароль',
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'username': 'Имя пользователя',
        'username_help': 'Если не введете, будет создано автоматически',
        'password_help': 'Если не введете, будет создано автоматически',
        'finish_registration': 'Завершить регистрацию',
        'otp_header': 'Код подтверждения',
        'otp_help': 'Введите код, отправленный на ваш телефон',
        'otp_sent_to': 'код отправлен на номер',
        'code_6_digits': '6-значный код',
        'resend_otp': 'Переотправить код',
        'complete_registration_details': 'Введите дополнительные данные (необязательно)',
        'forgot_password': 'Забыли пароль?',
        'remember_me': 'Запомнить меня',
        'no_account': 'У вас нет аккаунта?',
        'already_have_account': 'У вас уже есть аккаунт?',
        'step1_header': 'Введите номер телефона',
        'step2_header': 'Код подтверждения',
        'step3_header': 'Заполнение данных',

        // Profile
        'personal_info': 'Личная информация',
        'changeable': 'Можно изменить',
        'phone_not_changeable': 'Номер телефона нельзя изменить',
        'change_password': 'Изменить пароль',
        'current_password': 'Текущий пароль',
        'new_password': 'New Password:',
        'confirm_new_password': 'Confirm New Password:',
        'current_password_help': 'Введите текущий пароль, чтобы изменить пароль',
        'profile_stats': 'Статистика профиля',
        'registration_date': 'Дата регистрации',
        'account_status': 'Статус аккаунта',
        'last_activity': 'Последняя активность',
        'required': 'Обязательно',
        'available': 'Доступно',

        // Transfers
        'sent': 'Отправлено',
        'received': 'Получено',
        'create_transfer': 'Создать перевод',
        'transfer_info': 'Данные перевода',
        'receiver': 'Получатель',
        'make_transfer': 'Выполнить перевод',
        'transfer_details': 'Детали перевода',
        'sent_amount': 'Отправленная сумма',
        'received_amount': 'Полученная сумма',
        'created_at_text': 'создано',

        // Messages
        'no_data': 'Нет данных',
        'loading': 'Загрузка...',
        'success': 'Успешно',
        'error': 'Ошибка',
        'confirm_delete': 'Вы действительно хотите удалить?',
        'are_you_sure': 'Вы уверены?',

        // Wallet Forms
        'create_wallet': 'Создание нового кошелька',
        'edit_wallet': 'Редактировать кошелек',
        'delete_wallet': 'Удалить кошелек',
        'wallet_info': 'Данные кошелька',
        'initial_balance': 'Начальный баланс',
        'initial_balance_help': 'Если вы хотите добавить средства, введите сумму',
        'card_name_example': 'Например: "Моя карта Humo"',
        'wallet_not_found': 'Кошелек не найден',
        'wallet_name': 'Название кошелька',

        // Category Forms
        'create_category': 'Создание новой категории',
        'edit_category': 'Редактировать категорию',
        'delete_category': 'Удалить категорию',
        'category_info': 'Данные категории',
        'category_name_help': 'Например: "Зарплата", "Продукты"',
        'category_warning': 'Внимание! Все транзакции, относящиеся к этой категории, будут удалены.',
        'created_at': 'Дата создания',

        // Transaction Forms
        'new_income': 'Новый Доход',
        'new_expense': 'Новый Расход',
        'delete_transaction': 'Удалить транзакцию',
        'wallet_not_found_create_one': 'Кошелек не существует. Сначала создайте кошелек.',
        'description_help': 'Оставьте описание (необязательно)',
        'balance_check': 'Проверка баланса',
        'converted_amount': 'Конвертированная сумма',
        'sufficient_funds': 'Достаточно',
        'insufficient_funds': 'Недостаточно',
        'amount_required': 'Сумма обязательна',
        'wallet_balance_will_decrease': 'Баланс кошелька уменьшится',
        'wallet_balance_will_increase': 'Баланс кошелька увеличится',
        'attention': 'Внимание!',
        'wallet_info': 'Данные кошелька',
        'transaction_info': 'Данные транзакции',

        // Chat
        'chat_list': 'Список чатов',
        'chat_user': 'Пользователь',
        'status': 'Статус',
        'actions': 'Действия',
        'me': 'Я',
        'ago': 'назад',
        'oldin': 'назад',
        'latest_message': 'Последнее сообщение',
        'new_messages_count': 'новых',
        'closed': 'Закрыт',
        'open': 'Открыть',
        'no_messages': 'Сообщений нет',
        'start_chat_with_users': 'Начните чат с пользователями',
        'start_chat_with_user': 'Начните чат с пользователем',
        'user_info': 'Информация о пользователе',
        'user_status': 'Статус',
        'wallets_count': 'Количество кошельков',
        'open_in_admin_panel': 'Открыть в админ панели',
        'admin_name': 'Админ',
        'online': 'В сети',
        'offline': 'Не в сети',
        'start_chat_with_admin': 'Начните чат с админом',
        'chat_info': 'Информация о чате',
        'help_center': 'Центр помощи',
        'messages_count': 'Количество сообщений',
        'admin_reply_time_help': 'Ответ админа обычно приходит в течение 24 часов',
        'placeholder_message': 'Введите сообщение...',
    },

    en: {
        // App & Navigation
        'app_name': 'Finance App',
        'dashboard': 'Dashboard',
        'wallets': 'Wallets',
        'categories': 'Categories',
        'transactions': 'Transactions',
        'transfers': 'Transfers',
        'statistics': 'Statistics',
        'chat': 'Chat',
        'profile': 'Profile',
        'admin_panel': 'Admin Panel',
        'admin_dashboard': 'Admin Dashboard',
        'messages': 'Messages',
        'admin_with': 'with Admin',
        'go_to_django_admin': 'Go to Django Admin',
        'latest_message': 'Latest Message',
        'waiting_reply': 'Waiting for Reply',
        'replied': 'Replied',
        'logout': 'Logout',
        'login': 'Login',
        'register': 'Register',

        // Common Actions
        'add': 'Add',
        'create': 'Create',
        'edit': 'Edit',
        'update': 'Update',
        'delete': 'Delete',
        'save': 'Save',
        'cancel': 'Cancel',
        'filter': 'Filter',
        'search': 'Search',
        'view': 'View',
        'back': 'Back',
        'next': 'Next',
        'submit': 'Submit',
        'close': 'Close',
        'view_all': 'View All',
        'quick_actions': 'Quick Actions',

        // Wallet related
        'wallet': 'Wallet',
        'wallet_list': 'Wallet List',
        'add_wallet': 'Add Wallet',
        'wallet_type': 'Wallet Type',
        'cash': 'Cash',
        'card': 'Card',
        'card_number': 'Card Number',
        'card_type': 'Card Type',
        'humo': 'Humo',
        'uzcard': 'UzCard',
        'visa': 'Visa',
        'mastercard': 'MasterCard',
        'balance': 'Balance',
        'total_balance': 'Total Balance',
        'wallets_balance': 'Wallets Balance',
        'currency': 'Currency',
        'title': 'Title',
        'no_wallets': 'No Wallets',

        // Category related
        'category': 'Category',
        'category_list': 'Category List',
        'add_category': 'Add Category',
        'category_name': 'Category Name',
        'category_type': 'Category Type',
        'income': 'Income',
        'expense': 'Expense',
        'icon': 'Icon',

        // Transaction related
        'transaction': 'Transaction',
        'transaction_list': 'Transaction List',
        'recent_transactions': 'Recent Transactions',
        'transaction_history': 'Transaction History',
        'add_income': 'Add Income',
        'add_expense': 'Add Expense',
        'daily_income': 'Daily Income',
        'daily_expense': 'Daily Expense',
        'total_income': 'Total Income',
        'total_expense': 'Total Expense',
        'amount': 'Amount',
        'description': 'Description',
        'date': 'Date',
        'exchange_rate': 'Exchange Rate',
        'no_income': 'No Income',
        'no_expense': 'No Expense',

        // Transfer related
        'transfer': 'Transfer',
        'transfer_list': 'Transfer List',
        'add_transfer': 'Add Transfer',
        'from_wallet': 'From Wallet',
        'to_wallet': 'To Wallet',

        // Statistics
        'by_period_filter': 'Filter by Period',
        'select_period': 'Select Period',
        'period': 'Period',
        'daily': 'Daily',
        'weekly': 'Weekly',
        'monthly': 'Monthly',
        'yearly': 'Yearly',
        'custom': 'Custom Period',

        // Months
        'january': 'January',
        'february': 'February',
        'march': 'March',
        'april': 'April',
        'may': 'May',
        'june': 'June',
        'july': 'July',
        'august': 'August',
        'september': 'September',
        'october': 'October',
        'november': 'November',
        'december': 'December',
        'custom': 'Custom Range',
        'start_date': 'Start Date',
        'end_date': 'End Date',
        'period_range': 'period',
        'from': 'from',
        'to': 'to',
        'total_income': 'Total Income',
        'total_expense': 'Total Expense',
        'income_by_category': 'Income by Category',
        'expense_by_category': 'Expense by Category',
        'day': 'Day',
        'month': 'Month',
        'year': 'Year',
        'select_day': '--- Select Day ---',
        'select_month': '--- Select Month ---',
        'select_year': '--- Select Year ---',
        'no_income_data': 'No income data available',
        'no_expense_data': 'No expense data available',

        // Months
        'january': 'January',
        'february': 'February',
        'march': 'March',
        'april': 'April',
        'may': 'May',
        'june': 'June',
        'july': 'July',
        'august': 'August',
        'september': 'September',
        'october': 'October',
        'november': 'November',
        'december': 'December',

        // Auth
        'phone_number': 'Phone Number',
        'password': 'Password',
        'confirm_password': 'Confirm Password',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'username': 'Username',
        'username_help': 'If left blank, it will be generated automatically',
        'password_help': 'If left blank, it will be generated automatically',
        'finish_registration': 'Finish Registration',
        'otp_header': 'Verification Code',
        'otp_help': 'Enter the code sent to your phone',
        'otp_sent_to': 'code sent to',
        'code_6_digits': '6-digit code',
        'resend_otp': 'Resend Code',
        'complete_registration_details': 'Complete Registration Details (optional)',
        'forgot_password': 'Forgot Password?',
        'remember_me': 'Remember Me',
        'no_account': 'Don\'t have an account?',
        'already_have_account': 'Already have an account?',
        'step1_header': 'Enter phone number',
        'step2_header': 'Verification code',
        'step3_header': 'Complete registration',

        // Messages
        'no_data': 'No Data',
        'loading': 'Loading...',
        'success': 'Success',
        'error': 'Error',
        'confirm_delete': 'Are you sure you want to delete?',
        'are_you_sure': 'Are you sure?',

        // Wallet Forms
        'create_wallet': 'Create New Wallet',
        'edit_wallet': 'Edit Wallet',
        'delete_wallet': 'Delete Wallet',
        'wallet_info': 'Wallet Information',
        'initial_balance': 'Initial Balance',
        'initial_balance_help': 'If you want to add funds, enter the amount',
        'card_name_example': 'E.g.: "My Humo card"',
        'wallet_not_found': 'Wallet not found',
        'wallet_name': 'Wallet Name',

        // Category Forms
        'create_category': 'Create New Category',
        'edit_category': 'Edit Category',
        'delete_category': 'Delete Category',
        'category_info': 'Category Information',
        'category_name_help': 'E.g.: "Salary", "Groceries"',
        'category_warning': 'Attention! All transactions belonging to this category will be deleted.',
        'created_at': 'Created At',

        // Transaction Forms
        'new_income': 'New Income',
        'new_expense': 'New Expense',
        'delete_transaction': 'Delete Transaction',
        'wallet_not_found_create_one': 'No wallet found. Please create a wallet first.',
        'description_help': 'Leave a description (optional)',
        'balance_check': 'Balance check',
        'converted_amount': 'Converted amount',
        'sufficient_funds': 'Sufficient',
        'insufficient_funds': 'Insufficient',
        'amount_required': 'Amount is required',
        'wallet_balance_will_decrease': 'Wallet balance will decrease',
        'wallet_balance_will_increase': 'Wallet balance will increase',
        'attention': 'Attention!',
        'wallet_info': 'Wallet Information',
        'transaction_info': 'Transaction Information',
        'created_at_text': 'created at',

        // Chat
        'chat_list': 'Chat List',
        'chat_user': 'User',
        'status': 'Status',
        'actions': 'Actions',
        'me': 'Me',
        'ago': 'ago',
        'oldin': 'ago',
        'new_messages_count': 'new',
        'closed': 'Closed',
        'open': 'Open',
        'no_messages': 'No messages',
        'start_chat_with_users': 'Start a chat with users',
        'start_chat_with_user': 'Start a chat with the user',
        'user_info': 'User Information',
        'user_status': 'Status',
        'wallets_count': 'Wallets count',
        'open_in_admin_panel': 'Open in admin panel',
        'admin_name': 'Admin',
        'online': 'Online',
        'offline': 'Offline',
        'start_chat_with_admin': 'Start a chat with admin',
        'chat_info': 'Chat Information',
        'help_center': 'Help Center',
        'messages_count': 'Messages count',
        'admin_reply_time_help': 'Admin reply usually arrives within 24 hours',
        'placeholder_message': 'Write a message...',
        'new_password': 'New Password:',
        'confirm_new_password': 'Confirm New Password:',
    }
};

// Get translation for a key
function t(key, lang) {
    const currentLang = lang || localStorage.getItem('language') || 'uz';
    return translations[currentLang][key] || key;
}

// Change language
function changeLanguage(lang) {
    if (!translations[lang]) {
        console.error('Language not supported:', lang);
        return;
    }

    localStorage.setItem('language', lang);
    updatePageLanguage(lang);
    updateLanguageDisplay(lang);
}

// Update all elements with data-i18n attribute
function updatePageLanguage(lang) {
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = t(key, lang);

        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            if (element.type === 'button' || element.type === 'submit') {
                element.value = translation;
            } else {
                element.placeholder = translation;
            }
        } else if (element.tagName === 'OPTION') {
            element.textContent = translation;
        } else {
            element.textContent = translation;
        }
    });

    // Update HTML lang attribute
    document.documentElement.lang = lang;
}

// Update language display in dropdown
function updateLanguageDisplay(lang) {
    const langDisplay = document.getElementById('current-lang');
    if (langDisplay) {
        const langNames = {
            'uz': "O'zbek",
            'ru': 'Русский',
            'en': 'English'
        };
        langDisplay.textContent = langNames[lang] || "O'zbek";
    }

    // Update active state in dropdown
    const langButtons = document.querySelectorAll('[data-lang]');
    langButtons.forEach(btn => {
        if (btn.getAttribute('data-lang') === lang) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    const savedLang = localStorage.getItem('language') || 'uz';
    updatePageLanguage(savedLang);
    updateLanguageDisplay(savedLang);

    // Add click handlers to language buttons
    const langButtons = document.querySelectorAll('[data-lang]');
    langButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const newLang = this.getAttribute('data-lang');
            changeLanguage(newLang);
        });
    });
});
