
Attribute VB_Name = "RefreshModule"
Option Explicit

Public Sub RefreshAllLinks()
    On Error Resume Next
    Dim links As Variant
    links = ActiveWorkbook.LinkSources(Type:=xlLinkTypeExcelLinks)
    If Not IsEmpty(links) Then
        ActiveWorkbook.UpdateLink Name:=links, Type:=xlLinkTypeExcelLinks
    End If
    Application.CalculateFullRebuild
    MsgBox "All external links and formulas refreshed.", vbInformation, "Q-SMEC Chemistry Properties"
End Sub
