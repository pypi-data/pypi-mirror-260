import auto_anno_2 as aa
aa.config['api'] = 'openai'
# aa.config['openai']['key'] = 'sk-E9x1FQe8RYCLDZL6ru1tcjHT6d91unWhEdmhysIVJ8Veka0D'
# aa.config['openai']['api_base'] = 'https://api.aiproxy.io/v1'
aa.config['openai']['key'] = 'sk-jganxZoyZigB5qnK3725E223Ab97449198Ef9f287806E6D3'
aa.config['openai']['api_base'] = 'https://openkey.cloud/v1'
result = aa.cls('今天天气', ['天气', '股票'])
print(result)
