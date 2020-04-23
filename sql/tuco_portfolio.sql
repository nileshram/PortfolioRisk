select con.ExpirationDate, con.ExpirationMonth, con.Product, con.Symbol, con.Strike, con.PutCall, pos.Position  from Abn.dbo.Positions as pos
left outer join Abn.dbo.Accounts as acc on pos.FkAccountId=acc.Id
left outer join Abn.dbo.Contracts as con on pos.FkContractId=con.Id
where acc.FullAccountName in ('GBP_MM_FRONT_TUCO', 'EUR_MM_FRONT_TUCO')