// ============================================================================
// HR Analytics — STAR SCHEMA (Power Query / M)
// ----------------------------------------------------------------------------
// Builds a dimensional model instead of a single flat table, so DAX filter
// propagation works cleanly and slicers behave predictably.
//
//   DimDepartment ─┐
//   DimJobRole    ─┤
//   DimTenureBand ─┼── FactEmployee ── DimDate
//   DimIncomeBand ─┤
//   DimAgeBand    ─┤
//   DimOvertime   ─┘
//
// Grain of FactEmployee : one row per employee (EmployeeNumber)
// In Power BI: Home > Transform data > Advanced Editor > paste per query,
// or wrap in a single query and split. See docs/BUILD_GUIDE.md step 2.
// ============================================================================

// ---------------------------------------------------------------------------
// SHARED SOURCE — used by every query below
// ---------------------------------------------------------------------------
Raw = () =>
    let
        Src = Csv.Document(
            File.Contents("C:\POWER-BI-\data\HR_Employee_Attrition.csv"),
            [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]
        ),
        Promoted = Table.PromoteHeaders(Src, [PromoteAllScalars = true]),
        Typed = Table.TransformColumnTypes(
            Promoted,
            {
                {"Age", Int64.Type}, {"Attrition", type text},
                {"BusinessTravel", type text}, {"Department", type text},
                {"DistanceFromHome", Int64.Type}, {"Education", Int64.Type},
                {"EducationField", type text}, {"EmployeeNumber", Int64.Type},
                {"EnvironmentSatisfaction", Int64.Type}, {"Gender", type text},
                {"JobInvolvement", Int64.Type}, {"JobLevel", Int64.Type},
                {"JobRole", type text}, {"JobSatisfaction", Int64.Type},
                {"MaritalStatus", type text}, {"MonthlyIncome", Int64.Type},
                {"NumCompaniesWorked", Int64.Type}, {"OverTime", type text},
                {"PercentSalaryHike", Int64.Type}, {"PerformanceRating", Int64.Type},
                {"StockOptionLevel", Int64.Type}, {"TotalWorkingYears", Int64.Type},
                {"TrainingTimesLastYear", Int64.Type}, {"WorkLifeBalance", Int64.Type},
                {"YearsAtCompany", Int64.Type}, {"YearsInCurrentRole", Int64.Type},
                {"YearsSinceLastPromotion", Int64.Type},
                {"YearsWithCurrManager", Int64.Type}
            }
        )
    in
        Typed,

// ===========================================================================
// FACT TABLE
// ===========================================================================
FactEmployee =
let
    Base = Raw(),

    // Derived bands live on the fact so they can also be dims if needed
    WithBands = Table.AddColumn(Base, "TenureBand", each
        if [YearsAtCompany] < 1  then "1. <1 yr"   else
        if [YearsAtCompany] < 3  then "2. 1-2 yrs" else
        if [YearsAtCompany] < 6  then "3. 3-5 yrs" else
        if [YearsAtCompany] < 11 then "4. 6-10 yrs" else
        if [YearsAtCompany] < 21 then "5. 11-20 yrs" else "6. 20+ yrs",
        type text),

    WithIncome = Table.AddColumn(WithBands, "IncomeBand", each
        if [MonthlyIncome] < 3000  then "1. <3k"   else
        if [MonthlyIncome] < 5000  then "2. 3k-5k" else
        if [MonthlyIncome] < 8000  then "3. 5k-8k" else
        if [MonthlyIncome] < 12000 then "4. 8k-12k" else "5. 12k+",
        type text),

    WithAge = Table.AddColumn(WithIncome, "AgeBand", each
        if [Age] < 25 then "1. Under 25" else
        if [Age] < 35 then "2. 25-34"    else
        if [Age] < 45 then "3. 35-44"    else
        if [Age] < 55 then "4. 45-54"    else "5. 55+",
        type text),

    // Attrition as a 1/0 measure column keeps SUM() aggregation simple
    WithFlag = Table.AddColumn(WithAge, "LeftFlag", each
        if [Attrition] = "Yes" then 1 else 0, Int64.Type),

    WithAnnual = Table.AddColumn(WithFlag, "AnnualIncome", each
        [MonthlyIncome] * 12, Int64.Type),

    // ---- keep only fact columns + keys (dims hold the descriptive text) ----
    Keep = Table.SelectColumns(WithAnnual, {
        "EmployeeNumber", "Age", "AgeBand", "Department", "JobRole",
        "JobLevel", "OverTime", "BusinessTravel", "Education", "EducationField",
        "Gender", "MaritalStatus", "DistanceFromHome", "MonthlyIncome",
        "AnnualIncome", "IncomeBand", "YearsAtCompany", "TenureBand",
        "TotalWorkingYears", "NumCompaniesWorked", "YearsInCurrentRole",
        "YearsSinceLastPromotion", "YearsWithCurrManager", "StockOptionLevel",
        "PercentSalaryHike", "TrainingTimesLastYear", "Attrition", "LeftFlag",
        "EnvironmentSatisfaction", "JobSatisfaction", "JobInvolvement",
        "WorkLifeBalance", "PerformanceRating"
    }),

    Renamed = Table.RenameColumns(Keep, {{"Attrition", "Attrition Status"}}),

    // Data-quality gate: fail loudly if the source ever changes shape
    Guard = if Table.RowCount(Renamed) = 1470
            then Renamed
            else error "Expected 1,470 rows, found " & Text.From(Table.RowCount(Renamed))
in
    Guard,

// ===========================================================================
// DIMENSIONS
// ===========================================================================
DimDepartment =
let
    Base = Raw(),
    Grp = Table.Group(Base, {"Department"}, {
        {"Headcount", each Table.RowCount(_), Int64.Type}
    }),
    // prefix guarantees correct sort order in slicers
    WithKey = Table.AddColumn(Grp, "DeptSort", each
        if [Department] = "Human Resources"     then 1 else
        if [Department] = "Research & Development" then 2 else 3,
        Int64.Type),
    Typed = Table.TransformColumnTypes(WithKey, {{"DeptSort", Int64.Type}})
in
    Typed,

DimJobRole =
let
    Base = Raw(),
    Grp = Table.Group(Base, {"JobRole", "Department"}, {
        {"Headcount", each Table.RowCount(_), Int64.Type}
    }),
    WithSort = Table.AddColumn(Grp, "RoleSort", each
        if Text.StartsWith([JobRole], "Healthcare")    then 1 else
        if Text.StartsWith([JobRole], "Human")         then 2 else
        if Text.StartsWith([JobRole], "Laboratory")    then 3 else
        if Text.StartsWith([JobRole], "Manager")       then 4 else
        if Text.StartsWith([JobRole], "Manufacturing") then 5 else
        if Text.StartsWith([JobRole], "Research Dir")  then 6 else
        if Text.StartsWith([JobRole], "Research Sci")  then 7 else
        if Text.StartsWith([JobRole], "Sales Exec")    then 8 else 9,
        Int64.Type)
in
    WithSort,

DimTenureBand =
let
    Src = {
        [TenureBand = "1. <1 yr",     SortOrder = 1, MinYears = 0,  MaxYears = 0],
        [TenureBand = "2. 1-2 yrs",   SortOrder = 2, MinYears = 1,  MaxYears = 2],
        [TenureBand = "3. 3-5 yrs",   SortOrder = 3, MinYears = 3,  MaxYears = 5],
        [TenureBand = "4. 6-10 yrs",  SortOrder = 4, MinYears = 6,  MaxYears = 10],
        [TenureBand = "5. 11-20 yrs", SortOrder = 5, MinYears = 11, MaxYears = 20],
        [TenureBand = "6. 20+ yrs",   SortOrder = 6, MinYears = 21, MaxYears = 99]
    },
    Tbl = Table.FromRecords(Src)
in
    Tbl,

DimIncomeBand =
let
    Src = {
        [IncomeBand = "1. <3k",   SortOrder = 1, MinIncome = 0,    MaxIncome = 2999],
        [IncomeBand = "2. 3k-5k", SortOrder = 2, MinIncome = 3000, MaxIncome = 4999],
        [IncomeBand = "3. 5k-8k", SortOrder = 3, MinIncome = 5000, MaxIncome = 7999],
        [IncomeBand = "4. 8k-12k",SortOrder = 4, MinIncome = 8000, MaxIncome = 11999],
        [IncomeBand = "5. 12k+",  SortOrder = 5, MinIncome = 12000,MaxIncome = 99999]
    },
    Tbl = Table.FromRecords(Src)
in
    Tbl,

DimAgeBand =
let
    Src = {
        [AgeBand = "1. Under 25", SortOrder = 1, MinAge = 18, MaxAge = 24],
        [AgeBand = "2. 25-34",    SortOrder = 2, MinAge = 25, MaxAge = 34],
        [AgeBand = "3. 35-44",    SortOrder = 3, MinAge = 35, MaxAge = 44],
        [AgeBand = "4. 45-54",    SortOrder = 4, MinAge = 45, MaxAge = 54],
        [AgeBand = "5. 55+",      SortOrder = 5, MinAge = 55, MaxAge = 99]
    },
    Tbl = Table.FromRecords(Src)
in
    Tbl,

DimOvertime =
let
    Src = {[OverTime = "No", SortOrder = 1], [OverTime = "Yes", SortOrder = 2]}
in
    Table.FromRecords(Src),

// ===========================================================================
// RELATIONSHIPS  (set these in Model view — Power BI cannot infer them
// automatically because the dims are derived, not looked up)
// ===========================================================================
//   DimDepartment[Department]   1 ── * FactEmployee[Department]
//   DimJobRole[JobRole]         1 ── * FactEmployee[JobRole]
//   DimTenureBand[TenureBand]   1 ── * FactEmployee[TenureBand]
//   DimIncomeBand[IncomeBand]   1 ── * FactEmployee[IncomeBand]
//   DimAgeBand[AgeBand]         1 ── * FactEmployee[AgeBand]
//   DimOvertime[OverTime]       1 ── * FactEmployee[OverTime]
//
// Cross-filter direction: Single (dim -> fact) on all relationships.
// Set each dim's SortOrder column as the "Sort by column" for its band field.
