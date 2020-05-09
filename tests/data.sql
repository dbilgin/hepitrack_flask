INSERT INTO user (email, password, access_token, verified)
VALUES
	(
		'test',
		'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f',
		'$5$rounds=535000$FUkZUxfRNqJpJO17$eWS/9WCihkpOvqcr7HV1VJtJqjazu5NYHAlbqubPme1',
		0
	),
	(
		'other',
		'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79',
		'$5$rounds=535000$FUkZUxfRNqJpJO17$eWS/9WCihkpOvqcr7HV1VJtJqjazu5NYHAlbqubPme1',
		1
	);

INSERT INTO news (source, author, title, description, url, image, publish_date)
VALUES
  ('Hepitrack', 'dbilgin', 'Test', 'Description', 'www.hepitrack.com', 'image.jpg', '2020-05-07T20:11:41Z');
