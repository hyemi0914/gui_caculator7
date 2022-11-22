import sys
from PyQt5.QtWidgets import *

class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_first = QGridLayout()
        layout_second = QGridLayout()
        layout_third = QGridLayout()
        layout_equation_solution = QFormLayout()

        self.temp_number = 0
        self.temp_operator = ""

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        label_equation = QLabel("Equation: ")
        label_solution = QLabel("Number: ")
        self.equation = QLineEdit("")
        self.solution = QLineEdit("")

        self.number_display = QLineEdit("")

        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        # layout_equation_solution.addRow(label_equation, self.equation)
        # layout_equation_solution.addRow(label_solution, self.solution)
        layout_equation_solution.addRow(self.number_display)

        ### 사칙연상 버튼 생성
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_division = QPushButton("/")

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))

        ### 사칙연산 버튼을 layout_operation 레이아웃에 추가
        layout_third.addWidget(button_plus, 2, 3)
        layout_third.addWidget(button_minus, 1, 3)
        layout_third.addWidget(button_product, 0, 3)
        layout_second.addWidget(button_division, 1, 3)

        ### =, clear, backspace 버튼 생성
        button_equal = QPushButton("=")
        button_clear = QPushButton("Clear")
        button_backspace = QPushButton("Backspace")

        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        ### =, clear, backspace 버튼을 layout_clear_equal 레이아웃에 추가
        layout_first.addWidget(button_clear, 0, 1)
        layout_first.addWidget(button_backspace, 0, 3)
        layout_third.addWidget(button_equal, 3, 3)

        ### 제곱, 제곱근, 역수, 나머지, 값을 null로 설정하는 버튼 생성
        button_square = QPushButton("x^2")
        button_root = QPushButton("x^1/2")
        button_inverse = QPushButton("1/x")
        button_remainder = QPushButton("%")
        button_setnull = QPushButton("C")

        ### 제곱, 제곱근, 역수, 나머지, 값을 0으로 설정하는 버튼 클릭 시 시그널 설정
        button_square.clicked.connect(lambda state, operation = "x^2": self.button_operation_clicked(operation))
        button_root.clicked.connect(lambda state, operation = "x^1/2": self.button_operation_clicked(operation))
        button_inverse.clicked.connect(lambda state, operation = "1/x":self.button_operation_clicked(operation))
        button_remainder.clicked.connect(lambda state, operation = "%": self.button_operation_clicked(operation))
        button_setnull.clicked.connect(lambda state, operation = "C": self.button_operation_clicked(operation))

        ### 제곱, 제곱근, 역수, 나머지, 값을 null로 설정하는 버튼을 layout_operation 레이아웃에 추가
        layout_second.addWidget(button_square, 1, 1)
        layout_second.addWidget(button_root, 1, 2)
        layout_second.addWidget(button_inverse, 1, 0)
        layout_first.addWidget(button_remainder, 0, 0)
        layout_first.addWidget(button_setnull, 0, 2)

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))
            if number >0:
                x,y = divmod(number-1, 3)
                layout_third.addWidget(number_button_dict[number], x, y)
            elif number==0:
                layout_third.addWidget(number_button_dict[number], 3, 1)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_third.addWidget(button_dot, 3, 2)

        button_double_zero = QPushButton("00")
        button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))
        layout_third.addWidget(button_double_zero, 3, 0)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_first)
        main_layout.addLayout(layout_second)
        main_layout.addLayout(layout_third)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num):
        equation = self.number_display.text()
        equation += str(num)
        self.number_display.setText(equation)

    def button_operation_clicked(self, operation):
        # equation = self.number_display.text()
        # equation += operation
        # self.number_display.setText(equation)

        if operation not in ["C", "1/x", "x^2", "x^1/2"]:
            self.temp_number = float(self.number_display.text())
            self.number_display.setText("")

            self.temp_operator = operation

        else:
            if operation == "x^1/2":
                self.temp_number = float(self.number_display.text())
                self.temp_number = self.temp_number ** (1/2)
                self.number_display.setText(str(self.temp_number))
                pass

            if operation == "x^2":
                self.temp_number = float(self.number_display.text())
                self.temp_number = self.temp_number * self.temp_number
                self.number_display.setText(str(self.temp_number))
                pass

            if operation == "1/x":
                self.temp_number = float(self.number_display.text())
                self.temp_number = self.temp_number ** (-1)
                self.number_display.setText(str(self.temp_number))
                pass

            if operation == "C":
                self.temp_number = float(self.number_display.text())
                self.temp_number = ""
                self.number_display.setText(str(self.temp_number))
                pass

            self.temp_operator = ""
            self.temp_number = 0

    def button_equal_clicked(self):
        # equation = self.equation.text()
        # solution = eval(equation)
        # self.solution.setText(str(solution))

        temp_second_number = float(self.number_display.text())

        if self.temp_operator == "+":
            temp_result = self.temp_number + temp_second_number

        if self.temp_operator == "-":
            temp_result = self.temp_number - temp_second_number

        if self.temp_operator == "*":
            temp_result = self.temp_number * temp_second_number

        if self.temp_operator == "/":
            temp_result = self.temp_number / temp_second_number

        if self.temp_operator == "%":
            temp_result = self.temp_number % temp_second_number

        self.number_display.setText(str(temp_result))

        self.temp_operator = ""
        self.temp_number = 0

    def button_clear_clicked(self):
        # self.equation.setText("")
        self.number_display.setText("")

    def button_backspace_clicked(self):
        equation = self.number_display.text()
        equation = equation[:-1]
        self.number_display.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())