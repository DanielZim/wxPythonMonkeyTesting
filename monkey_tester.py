from random import randint


class Monkey_Tester():

    def __init__(self):
        self.current_click_position = None

    def generate_click(self, width, height, border):

        click_x = randint(border, width-border)
        click_y = randint(border, height-border)

        self.current_click_position = (click_x, click_y)

        return (click_x, click_y)

    def reset_current_click_position(self):
        self.current_click_position = None

    def is_click_position_on_widget(self, event_object):

        if not self.pointInRect(self.current_click_position, event_object.Rect):
            raise RuntimeError(
                "Click position not inside rectangle of " + str(event_object))

    def pointInRect(self, point, rect):
        x1, y1, w, h = rect.Get()
        x2, y2 = x1 + w, y1 + h
        x, y = point
        if x1 <= x and x <= x2:
            if y1 <= y and y <= y2:
                return True
        return False
