INSERT INTO channel (id,name) VALUES
	 ('731d752e-27df-47f5-908a-6c5ad10c19e3'::uuid,'email');

INSERT INTO plan (id,name,basic_monthly_rate,issue_fee) VALUES
	 ('845eb227-5356-4169-9799-95a97ec5ce33'::uuid,'EMPRESARIO',5000.00,50.00);

INSERT INTO plan (id,name,basic_monthly_rate,issue_fee) VALUES
	 ('4b921891-d08a-4436-b6c4-a63dd0dbdb94'::uuid,'EMPRENDEDOR',5000.00,50.00);

INSERT INTO plan (id,name,basic_monthly_rate,issue_fee) VALUES
	 ('41bc176b-8395-4f5b-b660-2cc9ca134a65'::uuid,'EMPRESARIO PLUS',5000.00,50.00);



INSERT INTO customer (id,document,name,plan_id,date_suscription) VALUES
	 ('845eb227-5356-4169-9799-95a97ec5ce33'::uuid,'900200195','Logan IT','845eb227-5356-4169-9799-95a97ec5ce33'::uuid,'2024-10-12 00:00:00.000');


INSERT INTO channel_plan (id,channel_id,plan_id) VALUES
	 ('b1b4fc06-1c63-4d27-94ac-c49cc3f7228c'::uuid,'731d752e-27df-47f5-908a-6c5ad10c19e3'::uuid,'845eb227-5356-4169-9799-95a97ec5ce33'::uuid);
