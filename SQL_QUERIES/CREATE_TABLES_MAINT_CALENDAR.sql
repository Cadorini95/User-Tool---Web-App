CREATE TABLE MAINT_CALENDAR (
    plant_id NVARCHAR(10),
    plant_name NVARCHAR(100),
    product NVARCHAR(10),
    initial_time DATETIME,
    final_time DATETIME,
    comment NVARCHAR(MAX)
);