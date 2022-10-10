import pandas as pd 
import design, result, sys, datetime
import ai_result as ai
import numpy as np
from PyQt5 import QtWidgets

class MainApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        self.cB_IL1b.addItems(["T/T", "T/C", "C/C"])
        self.cB_TNF.addItems(["G/G", "G/A", "A/A"])
        self.cB_APEX1.addItems(["T/T", "T/G", "G/G"])
        self.cB_XPD.addItems(["T/T", "T/G", "G/G"])
        self.cB_EGFR.addItems(["A/A", "A/T", "T/T"])
        self.cB_CHEK2.addItems(["N/N", "N/P", "P/P"])
        self.cB_TGFb1.addItems(["G/G", "G/C", "C/C"])
        self.cB_EPHX1.addItems(["T/T", "T/C", "C/C"])
        self.btn_Calc.clicked.connect(self.go_calc)

    def go_calc(self):
        isSmoking = self.is_Smoking.isChecked()
        isIL1b = self.is_IL1b.isChecked()
        isTNF = self.is_TNF.isChecked()
        isAPEX1 = self.is_APEX1.isChecked()
        isXPD = self.is_XPD.isChecked()
        isEGFR = self.is_EGFR.isChecked()
        isCHEK2 = self.is_CHEK2.isChecked()
        isTGFb1 = self.is_TGFb1.isChecked()
        isEPHX1 = self.is_EPHX1.isChecked()
        
        ai_help = ai.Forest_AI(is_smoking = isSmoking, is_Il1b = isIL1b,
        is_TNF = isTNF, is_APEX1 = isAPEX1,is_XPD = isXPD,
        is_EGFR = isEGFR, is_CHEK2 = isCHEK2, is_TGFb1 = isTGFb1, is_EPHX1 = isEPHX1)
        
        smoking = 1 if self.is_Smoking.isChecked() else 0
        data = []
        data.append(smoking)
        data.append(self.cB_IL1b.currentText())
        data.append(self.cB_TNF.currentText())
        data.append(self.cB_APEX1.currentText())
        data.append(self.cB_XPD.currentText())
        data.append(self.cB_EGFR.currentText())
        data.append(self.cB_CHEK2.currentText())
        data.append(self.cB_TGFb1.currentText())
        data.append(self.cB_EPHX1.currentText())

        df = pd.DataFrame(np.array([data]), columns=['Smoking', 'IL1b', 'TNF', 'APEX1', 'XPD', 'EGFR', 'CHEK2', 'TGFb1', 'EPHX1 '])
        #Il1b +
        df = df.replace(ai.replace_IL1b) if isIL1b else df.drop(list(ai.replace_IL1b.keys())[0], axis = 1)
        #TNF +
        df = df.replace(ai.replace_TNF) if isTNF else df.drop(list(ai.replace_TNF.keys())[0], axis = 1)
        #APEX1 +
        df = df.replace(ai.replace_APEX1) if isAPEX1 else df.drop(list(ai.replace_APEX1.keys())[0], axis = 1)
        #XPD +
        df = df.replace(ai.replace_XPD) if isXPD else df.drop(list(ai.replace_XPD.keys())[0], axis = 1)
        #EGFR +
        df = df.replace(ai.replace_EGFR) if isEGFR else df.drop(list(ai.replace_EGFR.keys())[0], axis = 1)
        #CHEK2 +
        df = df.replace(ai.replace_CHEK2) if isCHEK2 else df.drop(list(ai.replace_CHEK2.keys())[0], axis = 1)
        #TGFb1 +
        df = df.replace(ai.replace_TGFb1) if isTGFb1 else df.drop(list(ai.replace_TGFb1.keys())[0], axis = 1)
        #EPHX1 +
        df = df.replace(ai.replace_EPHX1) if isEPHX1 else df.drop(list(ai.replace_EPHX1.keys())[0], axis = 1)
        
        score = ai_help.train()
        res = ai_help.calc_Answer(df)
        self.result_window = ResultWindow(self.textName.text(), self.textAge.text(), res, score = score)
        self.result_window.show()
        


class ResultWindow(QtWidgets.QWidget, result.Ui_Result):
    def __init__(self, name, age, result_bool, staff = "Рубанович В.И.", score = None):
        super().__init__()
        self.setupUi(self) 
        self.textAge.setText(age)
        self.textFIO.setText(name) 
        res = "Выявлены генетические маркеры высокого риска рака легкого." if result_bool else "Генетические маркеры высокого риска рака легкого не выявлены."
        res = res + f"\nТочность прогноза: {score*100:.{1}f}" if score else res
        self.textResult.setText(res)
        self.textStaff.setText(staff)
        self.textData.setText(str(datetime.date.today()))
        self.btn.clicked.connect(self.close_window)

    def close_window(self):
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()