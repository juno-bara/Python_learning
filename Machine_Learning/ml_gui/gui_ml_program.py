from PyQt5.QtWidgets import *
import sys, pickle
from PyQt5 import uic , QtWidgets
import pandas as pd
import table_display
from sklearn.preprocessing import LabelEncoder ,StandardScaler , MinMaxScaler , PowerTransformer

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.Browse = self.findChild(QPushButton , "Browse")
        self.columns = self.findChild(QListWidget,"column_list")
        self.Submit_btn = self.findChild(QPushButton , "Submit")
        self.target_col = self.findChild(QLabel,"target_col")
        self.shape = self.findChild(QLabel , "shape")
        self.scale_btn = self.findChild(QPushButton , "scale_btn")
        self.tableView = self.findChild(QTableView , "tableView")

        self.cat_column = self.findChild(QComboBox , "cat_column")
        self.drop_column = self.findChild(QComboBox , "drop_column")
        self.empty_column = self.findChild(QComboBox , "empty_column")
        self.convert_btn = self.findChild(QPushButton , "convert_btn")
        self.drop_btn = self.findChild(QPushButton , "drop_btn")
        self.fiil_mean = self.findChild(QPushButton , "fiil_mean")
        self.fill_na = self.findChild(QPushButton , "fill_na")

        

        self.Browse.clicked.connect(self.get_csv)
        self.columns.clicked.connect(self.target)
        self.Submit_btn.clicked.connect(self.set_target)
        
        # fillna 처리 
        self.fiil_mean.clicked.connect(self.fillmean)
        self.fill_na.clicked.connect(self.fillna_func)

        # tocategorical 처리
        self.convert_btn.clicked.connect(self.convert_category)

        # column drop
        self.drop_btn.clicked.connect(self.dropc)

        #정규화
        self.scaler = self.findChild(QComboBox , "scaler")
        self.scale_btn = self.findChild(QPushButton , "scale_btn")

        self.scale_btn.clicked.connect(self.scale_value)

    def get_empty_list(self , df):
        empty_list= []
        for i in df.columns:
            if (df[i].isnull().values.any() == True):
                empty_list.append(i)
        return empty_list

    def filldetails(self, flag = 1):
        if (flag == 0):
            self.df = pd.read_csv(self.filepath,index_col=0, encoding='utf-8')
        
        self.columns.clear()
        self.column_list = []
        for i in self.df.columns:
            self.column_list.append(i)
        
        for i , j in enumerate(self.column_list):
            stri = f'{j} ------- {self.df[j].dtype}'
            self.columns.insertItem(i, stri)
        
        # print(self.column_list)

        self.cat_column.clear()
        self.cat_column.addItems(self.column_list)
        self.drop_column.clear()
        self.drop_column.addItems(self.column_list)
        self.empty_column.clear()
        self.empty_column.addItems(self.get_empty_list(self.df))
        


        x = table_display.DataFrameModel(self.df)
        self.tableView.setModel(x)
    
    def scale_value(self):
        x = self.df.drop(self.target_value, axis=1)
        scaler = self.scaler.currentText()
        if scaler == "StandardScale":
            scaled_features = StandardScaler().fit_transform(x)
            scaled_features_df = pd.DataFrame(scaled_features, index=x.index, columns=x.columns )
            scaled_features_df[self.target_value] = self.df[self.target_value]
            self.df = scaled_features_df
            self.filldetails()
        elif scaler == "MinMaxScale":
            scaled_features = MinMaxScaler().fit_transform(x)
            scaled_features_df = pd.DataFrame(scaled_features, index=x.index, columns=x.columns )
            scaled_features_df[self.target_value] = self.df[self.target_value]
            self.df = scaled_features_df
            self.filldetails()
        else :
            scaled_features = PowerTransformer().fit_transform(x)
            scaled_features_df = pd.DataFrame(scaled_features, index=x.index, columns=x.columns )
            scaled_features_df[self.target_value] = self.df[self.target_value]
            self.df = scaled_features_df
            self.filldetails()

    def dropc(self):
        if (self.drop_column.currentText() == self.target_value):
            self.target_value =""
            self.target_col.setText("")
        current_column = self.drop_column.currentText()
        self.df.drop(current_column, axis=1, inplace=True)
        self.filldetails()

    def convert_category(self):
        current_column = self.cat_column.currentText()
        self.df[current_column] = LabelEncoder().fit_transform(self.df[current_column])
        self.filldetails()

    def fillmean(self):
        current_column = self.empty_column.currentText()
        self.df[current_column] = self.df[current_column].fillna(self.df[current_column].mean())
        self.filldetails()

    def fillna_func(self):
        current_column = self.empty_column.currentText()
        self.df[current_column] = self.df[current_column].fillna(0)
        self.filldetails()

    def target(self):
        self.item = self.columns.currentItem().text().split()[0]
        print(self.item)

    def set_target(self):
        self.target_value = self.item
        self.target_col.setText(self.target_value)

    def get_csv(self):
        self.filepath , _ = QFileDialog.getOpenFileName(self, 'Open Csv File', '',"csv(*.csv)")
        # print(self.data)
        
        # print(df.info())
        self.filldetails(flag=0)
        # self.show()

   
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()

    sys.exit(app.exec_())