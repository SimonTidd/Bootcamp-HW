Attribute VB_Name = "Module1"
' note, I was getting a division by zero error when calculating the percent change for one stock (PLNT) so I added a condition for checking that
' I only did it for the case when it was not the last stock in a sheet
' what I would do going forward is some data cleaning steps before to avoid having to do this piecemeal


Sub ticker_total():
Dim Row_count As Long
Dim Stock_volume_bucket As Double
Dim Ticker_symbol As String
Dim print_row As Integer
Worksheets(1).Activate
For Page_counter = 1 To ThisWorkbook.Worksheets.Count
print_row = 2
Worksheets(Page_counter).Activate
Cells(1, 9).Value = "Ticker"
Cells(1, 10).Value = "Yearly Change"
Cells(1, 11).Value = "Percent Change"
Cells(1, 12).Value = "Total Stock Volume"
Row_count = Cells(Rows.Count, 1).End(xlUp).Row
Stock_volume_bucket = Cells(2, 7)
stock_year_open = Cells(2, 3)
Ticker_symbol = Cells(2, 1)
    For row_counter = 3 To Row_count
        If row_counter < Row_count And Cells(row_counter, 1).Value = Cells(row_counter - 1, 1).Value Then
        Stock_volume_bucket = Stock_volume_bucket + Cells(row_counter, 7)
        End If
        
        If row_counter < Row_count And Cells(row_counter, 1).Value <> Cells(row_counter - 1, 1).Value Then
        Cells(print_row, 9).Value = Ticker_symbol
        Cells(print_row, 12).Value = Stock_volume_bucket
        Cells(print_row, 10).Value = stock_year_open - Cells(row_counter - 1, 6)
        End If
        
        
        If row_counter < Row_count And Cells(row_counter, 1).Value <> Cells(row_counter - 1, 1).Value And stock_year_open > 0 Then
        Cells(print_row, 11).Value = (stock_year_open - Cells(row_counter - 1, 6)) / stock_year_open
        Cells(print_row, 11).NumberFormat = "0.00%"
        End If
        
        If row_counter < Row_count And Cells(row_counter, 1).Value <> Cells(row_counter - 1, 1).Value Then
        Ticker_symbol = Cells(row_counter, 1)
        Stock_volume_bucket = Cells(row_counter, 7)
        stock_year_open = Cells(row_counter, 3)
        print_row = print_row + 1
        End If
        
        If row_counter = Row_count And Cells(row_counter, 1).Value = Cells(row_counter - 1, 1).Value Then
        Stock_volume_bucket = Stock_volume_bucket + Cells(row_counter, 7)
        Cells(print_row, 9).Value = Ticker_symbol
        Cells(print_row, 12).Value = Stock_volume_bucket
        Cells(print_row, 10).Value = stock_year_open - Cells(row_counter, 6)
        Cells(print_row, 11).Value = (stock_year_open - Cells(row_counter, 6)) / stock_year_open
        Cells(print_row, 11).NumberFormat = "0.00%"
        End If
        
        
        If row_counter = Row_count And Cells(row_counter, 1).Value <> Cells(row_counter - 1, 1).Value Then
        Cells(print_row, 9).Value = Ticker_symbol
        Cells(print_row, 12).Value = Stock_volume_bucket
        Cells(print_row, 10).Value = Cells(row_counter, 3) - Cells(row_counter, 6)
        Cells(print_row, 11).Value = (Cells(row_counter, 3) - Cells(row_counter, 6)) / Cells(row_counter, 3)
        Cells(print_row, 11).NumberFormat = "0.00%"
        End If

        
    Next row_counter
    
    For row_counter = 2 To print_row
        If Cells(row_counter, 10).Value < 0 Then
        Cells(row_counter, 10).Interior.ColorIndex = 3
        Else
        Cells(row_counter, 10).Interior.ColorIndex = 4
        End If
    Next row_counter
    

    
    Dim highest_per_inc_val As Double
    Dim highest_per_dec_val As Double
    Dim highest_volume_val As Double
    Dim highest_per_inc_name As String
    Dim highest_per_dec_name As String
    Dim highest_volume_inc_name As String
      
    highest_per_inc_val = Cells(2, 10)
    highest_per_dec_val = Cells(2, 10)
    highest_volume_val = Cells(2, 12)
    highest_per_inc_name = Cells(2, 9)
    highest_per_dec_name = Cells(2, 9)
    highest_volume_name = Cells(2, 9)
    
    For summary_counter = 3 To Cells(10, Columns.Count).End(xlToLeft).Column
    If Cells(summary_counter, 11) > highest_per_inc_val Then
    highest_per_inc_val = Cells(summary_counter, 11)
    highest_per_inc_name = Cells(summary_counter, 9)
    End If
    
    If Cells(summary_counter, 11) < highest_per_dec_val Then
    highest_per_dec_val = Cells(summary_counter, 11)
    highest_per_dec_name = Cells(summary_counter, 9)
    End If
    
    If Cells(summary_counter, 12) > highest_volume_val Then
    highest_volume_val = Cells(summary_counter, 12)
    highest_volume_name = Cells(summary_counter, 9)
    End If
   
    Cells(2, 15).Value = "Greatest % Increase"
    Cells(3, 15).Value = "Greatest % Decrease"
    Cells(4, 15).Value = "Greatest Total Volume"
    Cells(2, 16).Value = highest_per_inc_name
    Cells(3, 16).Value = highest_per_dec_name
    Cells(4, 16).Value = highest_volume_name
    Cells(2, 17).Value = highest_per_inc_val
    Cells(3, 17).Value = highest_per_dec_val
    Cells(4, 17).Value = highest_volume_val
    Cells(1, 16).Value = "Ticker"
    Cells(1, 17).Value = "Value"
    Next summary_counter
Next Page_counter


End Sub




