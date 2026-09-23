// ============================================================================
// HR Analytics Dashboard — Power Query (M) Transformation
// ----------------------------------------------------------------------------
// In Power BI Desktop: Home > Transform data > Advanced Editor > paste this
// after changing the Source FilePath to point at data/HR_Employee_Attrition.csv
//
// What this query does:
//   1. Loads the raw CSV
//   2. Removes the 4 constant / non-informative columns
//   3. Converts coded 1-5 survey fields into readable labels
//   4. Adds derived columns used by the dashboard
// ============================================================================

let
    // 1. SOURCE -----------------------------------------------------------
    Source = Csv.Document(
        File.Contents("C:\POWER-BI-\data\HR_Employee_Attrition.csv"),
        [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
    ),

    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),

    // 2. SET COLUMN TYPES -------------------------------------------------
    Typed = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"Age", Int64.Type},
            {"Attrition", type text},
            {"BusinessTravel", type text},
            {"DailyRate", Int64.Type},
            {"Department", type text},
            {"DistanceFromHome", Int64.Type},
            {"Education", Int64.Type},
            {"EducationField", type text},
            {"EmployeeNumber", Int64.Type},
            {"EnvironmentSatisfaction", Int64.Type},
            {"Gender", type text},
            {"JobInvolvement", Int64.Type},
            {"JobLevel", Int64.Type},
            {"JobRole", type text},
            {"JobSatisfaction", Int64.Type},
            {"MaritalStatus", type text},
            {"MonthlyIncome", Int64.Type},
            {"NumCompaniesWorked", Int64.Type},
            {"OverTime", type text},
            {"PercentSalaryHike", Int64.Type},
            {"PerformanceRating", Int64.Type},
            {"StockOptionLevel", Int64.Type},
            {"TotalWorkingYears", Int64.Type},
            {"TrainingTimesLastYear", Int64.Type},
            {"WorkLifeBalance", Int64.Type},
            {"YearsAtCompany", Int64.Type},
            {"YearsInCurrentRole", Int64.Type},
            {"YearsSinceLastPromotion", Int64.Type},
            {"YearsWithCurrManager", Int64.Type}
        }
    ),

    // 3. DROP CONSTANT COLUMNS -------------------------------------------
    // EmployeeCount = 1 for every row, StandardHours = 80, Over18 = "Y".
    // They carry zero analytical signal and clutter the field list.
    RemovedConstants = Table.RemoveColumns(
        Typed,
        {"EmployeeCount", "StandardHours", "Over18", "HourlyRate", "MonthlyRate", "DailyRate"}
    ),

    // 4. LABEL THE CODED SURVEY FIELDS ------------------------------------
    // 1-4 satisfaction scales become readable text for the legend/filters.
    EducationLabeled = Table.TransformColumns(
        RemovedConstants,
        {
            "Education",
            each Text.Combine(
                {
                    if _ = 1 then "Below College"
                    else if _ = 2 then "College"
                    else if _ = 3 then "Bachelor"
                    else if _ = 4 then "Master"
                    else "Doctor"
                },
                ""
            ),
            type text
        }
    ),

    SatisfactionLabeled = Table.TransformColumns(
        EducationLabeled,
        {
            {"EnvironmentSatisfaction", each if _ = 1 then "Low" else if _ = 2 then "Medium" else if _ = 3 then "High" else "Very High", type text},
            {"JobSatisfaction",      each if _ = 1 then "Low" else if _ = 2 then "Medium" else if _ = 3 then "High" else "Very High", type text},
            {"JobInvolvement",       each if _ = 1 then "Low" else if _ = 2 then "Medium" else if _ = 3 then "High" else "Very High", type text},
            {"WorkLifeBalance",      each if _ = 1 then "Bad" else if _ = 2 then "Good" else if _ = 3 then "Better" else "Best",         type text},
            {"PerformanceRating",    each if _ = 3 then "Excellent" else "Outstanding",                                                    type text}
        }
    ),

    // 5. DERIVED COLUMNS FOR THE DASHBOARD --------------------------------
    AddAnnualIncome = Table.AddColumn(
        SatisfactionLabeled,
        "AnnualIncome",
        each [MonthlyIncome] * 12,
        Int64.Type
    ),

    AddAgeBand = Table.AddColumn(
        AddAnnualIncome,
        "AgeBand",
        each if [Age] < 25 then "Under 25"
             else if [Age] <= 34 then "25 - 34"
             else if [Age] <= 44 then "35 - 44"
             else if [Age] <= 54 then "45 - 54"
             else "55+",
        type text
    ),

    AddTenureBand = Table.AddColumn(
        AddAgeBand,
        "TenureBand",
        each if [YearsAtCompany] < 2 then "0-2 yrs"
             else if [YearsAtCompany] < 5 then "3-4 yrs"
             else if [YearsAtCompany] < 10 then "5-9 yrs"
             else if [YearsAtCompany] < 20 then "10-19 yrs"
             else "20+ yrs",
        type text
    ),

    // 6. RENAME FOR CLARITY & SORT ----------------------------------------
    Renamed = Table.RenameColumns(
        AddTenureBand,
        {{"Attrition", "Attrition Status"}}
    ),

    // Explicit sort order so band columns chart left-to-right correctly.
    Sorted = Table.Sort(Renamed, {{"EmployeeNumber", Order.Ascending}}),

    // 7. DATA QUALITY CHECK ----------------------------------------------
    // Fails loudly if the row count ever drifts from the expected 1,470.
    CheckedRows = if Table.RowCount(Sorted) = 1470
                  then Sorted
                  else error "Expected 1,470 rows, found " & Text.From(Table.RowCount(Sorted)),

    // Name the final query so DAX measures can reference 'Employees'
    Final = CheckedRows
in
    Final
