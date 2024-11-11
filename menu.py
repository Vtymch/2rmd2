import pygame
import sys
import math
 
# Инициализация Pygame
pygame.init()
 
# Основные настройки экрана
WIDTH, HEIGHT = 960, 600
FPS = 60  # Частота кадров
 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Test")
 
# Загрузка и изменение размера фона
main_background = pygame.image.load("imagesdanya/background1.jpg")
main_background = pygame.transform.scale(main_background, (WIDTH, HEIGHT))
 
# Загрузка изображений для кнопок
bone_button_img = pygame.image.load("imagesdanya/bone_normal.png")  # Обычная кнопка
bone_button_hover_img = pygame.image.load("imagesdanya/bone_hover.png")  # При наведении
bone_button_click_img = pygame.image.load("imagesdanya/bone_click.png")  # При нажатии
 
# Изменение размеров изображений кнопок
button_width, button_height = 250, 150
bone_button_img = pygame.transform.scale(bone_button_img, (button_width, button_height))
bone_button_hover_img = pygame.transform.scale(bone_button_hover_img, (button_width, button_height))
bone_button_click_img = pygame.transform.scale(bone_button_click_img, (button_width, button_height))
 
# Загрузка изображения курсора
sword_cursor_img = pygame.image.load("imagesdanya/sword_cursor.png")  # Кастомный курсор
sword_cursor_img = pygame.transform.scale(sword_cursor_img, (32, 32))  # Изменение размера курсора
 
# Доступные языки
languages = ["Русский", "English", "Norsk"]
language_index = 0  # Текущий индекс языка
 
# Переводы кнопок на разные языки
translations = {
    "new_game": {"Русский": "Новая игра", "English": "New Game", "Norsk": "Nytt spill"},
    "settings": {"Русский": "Настройки", "English": "Settings", "Norsk": "Innstillinger"},
    "exit": {"Русский": "Выход", "English": "Exit", "Norsk": "Avslutt"},
    "back": {"Русский": "Назад", "English": "Back", "Norsk": "Tilbake"},
    "language": {"Русский": "Язык", "English": "Language", "Norsk": "Språk"}
}
 
# Функция для смены языка
def change_language():
    global language_index
    language_index = (language_index + 1) % len(languages)  # Циклически меняем язык
    update_button_texts()
 
# Обновление текста кнопок при смене языка
def update_button_texts():
    current_language = languages[language_index]
    print(f"Updating buttons for language: {current_language}")
    main_menu_buttons[0].text = translations["new_game"][current_language]
    main_menu_buttons[1].text = translations["settings"][current_language]
    main_menu_buttons[2].text = translations["exit"][current_language]
    language_button.text = translations["language"][current_language]
    back_button.text = translations["back"][current_language]
   
    for button in main_menu_buttons + settings_buttons + new_game_buttons:
        button.update()  # Обновляем текст на кнопках

# Класс для кнопки с анимацией масштабирования
class ImageButton:
    def __init__(self, x, y, image, hover_image, click_image, text, action):
        self.original_image = image
        self.hover_image = hover_image
        self.click_image = click_image
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.action = action
        self.text = text
        self.font = pygame.font.SysFont(None, 40)
        self.text_surf = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)
 
        # Настройки анимации
        self.scale_factor = 1.0  # Текущий масштаб
        self.scale_speed = 0.05  # Скорость изменения масштаба
        self.is_hovered = False  # Флаг, отслеживающий, наведен ли курсор
 
    def draw(self, screen):
        # Отрисовка кнопки и текста с учетом масштаба
        scaled_image = pygame.transform.scale(self.image,
            (int(button_width * self.scale_factor), int(button_height * self.scale_factor)))
        scaled_rect = scaled_image.get_rect(center=self.rect.center)
 
        screen.blit(scaled_image, scaled_rect)
        self.text_rect = self.text_surf.get_rect(center=scaled_rect.center)
        screen.blit(self.text_surf, self.text_rect)
 
    def handle_event(self, event):
        # Обработка событий кнопки
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.is_hovered = True  # Наведение на кнопку
            else:
                self.is_hovered = False  # Уход с кнопки
 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.image = self.click_image  # Изменение при нажатии
 
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()  # Выполнение действия при отпускании кнопки
            self.image = self.original_image  # Возвращение в обычное состояние
 
    def update(self):
        # Анимация масштабирования
        if self.is_hovered:
            if self.scale_factor < 1.2:  # Ограничиваем максимальный размер
                self.scale_factor += self.scale_speed
        else:
            if self.scale_factor > 1.0:  # Возвращаемся к обычному размеру
                self.scale_factor -= self.scale_speed
        # Обновление текста
        self.text_surf = self.font.render(self.text, True, (0, 0, 0))
 
def fade_transition(new_state):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill((0, 0, 0))
 
    for alpha in range(0, 255, 15):
        fade_surface.set_alpha(alpha)
        draw_current_state()
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(20)
 
    global current_state
    current_state = new_state
 
    for alpha in range(255, -1, -15):
        fade_surface.set_alpha(alpha)
        draw_current_state()
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(20)
 
def draw_shadow_effect():
    # Создание полупрозрачной тени, имитируя эффект колебания лампы
    shadow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shadow_alpha = int(50 + 50 * math.sin(pygame.time.get_ticks() / 500.0))  # Колебание прозрачности
    shadow_surface.fill((0, 0, 0, shadow_alpha))  # Изменение прозрачности тени
    screen.blit(shadow_surface, (0, 0))
 
def draw_current_state():
    screen.blit(main_background, (0, 0))
    draw_shadow_effect()  # Добавление тени

    if current_state == "main_menu":
        draw_buttons(main_menu_buttons)
    elif current_state == "settings":
        update_button_texts()
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont(None, 55)
        text_surface = font.render(translations["settings"][languages[language_index]], True, (0, 0, 0))
        screen.blit(text_surface, (100, 200))
        draw_buttons(settings_buttons)
    elif current_state == "new_game":
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont(None, 55)
        text_surface = font.render(translations["new_game"][languages[language_index]], True, (0, 0, 0))
        screen.blit(text_surface, (100, 200))
        draw_buttons(new_game_buttons)
 
def draw_buttons(buttons):
    for button in buttons:
        button.update()  
        button.draw(screen)
 
def draw_cursor():
    cursor_x, cursor_y = pygame.mouse.get_pos()
    screen.blit(sword_cursor_img, (cursor_x - sword_cursor_img.get_width() // 2, cursor_y - sword_cursor_img.get_height() // 2))
 
def handle_events(buttons):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        for button in buttons:
            button.handle_event(event)
 
# Основной цикл игры
def game_loop():
    clock = pygame.time.Clock()
    while True:
        draw_current_state()
 
        if current_state == "main_menu":
            handle_events(main_menu_buttons)
        elif current_state == "settings":
            handle_events(settings_buttons)
        elif current_state == "new_game":
            handle_events(new_game_buttons)
 
        draw_cursor()
        pygame.display.update()
        clock.tick(FPS)
 
 
if __name__ == "__main__":
    current_state = "main_menu"
 
    # Устанавливаем первый язык как английский
    language_index = 0  # 0 соответствует "en" (английскому языку)
 
    # Основные кнопки
    main_menu_buttons = [
        ImageButton(WIDTH // 2, HEIGHT // 2 - 100, bone_button_img, bone_button_hover_img, bone_button_click_img, translations["new_game"][languages[language_index]], lambda: fade_transition("new_game")),
        ImageButton(WIDTH // 2, HEIGHT // 2, bone_button_img, bone_button_hover_img, bone_button_click_img, translations["settings"][languages[language_index]], lambda: fade_transition("settings")),
        ImageButton(WIDTH // 2, HEIGHT // 2 + 100, bone_button_img, bone_button_hover_img, bone_button_click_img, translations["exit"][languages[language_index]], sys.exit),
    ]
 
    # Кнопка для смены языка
    language_button = ImageButton(WIDTH // 2, HEIGHT // 2 + 200, bone_button_img, bone_button_hover_img, bone_button_click_img, translations["language"][languages[language_index]], change_language)
 
    # Кнопка "Назад" для других меню
    back_button = ImageButton(WIDTH // 2, 50, bone_button_img, bone_button_hover_img, bone_button_click_img, translations["back"][languages[language_index]], lambda: fade_transition("main_menu"))
 
    settings_buttons = [back_button, language_button]
    new_game_buttons = [back_button]
 
def show_menu():
    global current_state
    current_state = 'main_menu'

    while current_state == 'main_menu':
        draw_current_state()
        handle_events(main_menu_buttons)
        draw_cursor()
        pygame.display.update()
        
game_loop()   

 
 