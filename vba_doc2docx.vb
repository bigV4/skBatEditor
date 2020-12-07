Sub doc2docx()  'doc文件转docx文件
Dim myDialog As FileDialog, oFile As Variant
Set myDialog = Application.FileDialog(msoFileDialogFilePicker)
With myDialog
        .Filters.Clear    '清除所有文件筛选器中的项目
        .Filters.Add "所有 WORD97-2003 文件", "*.doc", 1    '增加筛选器的项目为所有WORD97-2003文件
        .AllowMultiSelect = True    '允许多项选择
        If .Show = -1 Then    '确定
            For Each oFile In .SelectedItems    '在所有选取项目中循环
                With Documents.Open(oFile)
.ComputeStatistics (wdStatisticPages)
                .SaveAs FileName:=oFile + "x", FileFormat:=wdFormatXMLDocument
                .Close
                End With
            Next
        End If
End With
End Sub
'一次选中单个、多个指定的doc文件转换
'打开word，Alt+F11进入VBA编辑界面，插入>模块，将下面代码帖进去，按F5即可