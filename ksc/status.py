from ksc.sorter import Sorter
from db.models import SuspectHost

class Status:
	def __init__(self, host_dict):
		self.sorted_dict = Sorter(host_dict=host_dict).get_reuslt_dict()

	def get_suspect_host(self):
		SuspectHost.objects.all().delete()
		for host in self.sorted_dict:
			if self.suspect_status(self.sorted_dict.get(host)):
				host_status = self.get_full_info(self.sorted_dict.get(host))
				host_obj = SuspectHost(host_name=host, 
									host_in_lan=host_status[0],
									agent_install=host_status[1], 
									agent_active=host_status[2], 
									instance_protect=host_status[3],)
				host_obj.save()

	def suspect_status(self, status_new):
		five_bit_digit_list_new = self.make_five_bit_digit(list(self.get_bin_digit(status_new)))
		if five_bit_digit_list_new[5]==1 and five_bit_digit_list_new[3]==0:
            # Хост включен и Агент не установлен
			return True
		if five_bit_digit_list_new[5]==1 and (five_bit_digit_list_new[2]==0 or five_bit_digit_list_new[1]==0):
            # Хост включен и (Агент не активен или постоянная защита не установлена) вне зависимости от установленности агента
			return True
		return False

	def make_five_bit_digit(self, bin_digit_list:list):
		for i in range(6-len(bin_digit_list)):
			bin_digit_list.insert(0,'0')
		five_bit_digit_list = list(map(int,bin_digit_list))
		return five_bit_digit_list

	def get_bin_digit(self, status):
		return str(bin(status)).replace('0b','')
	
	def get_full_info(self, status):
		'''Получаем всю инфу по статусу хоста'''
		five_bit_digit = self.make_five_bit_digit(list(self.get_bin_digit(status)))
		message = ['Видимость хоста:',
					'',
					'Агент администрирования установлен:',
					'Агент администрирования активен:',
					'Установлена постоянная защита:',
					'Компьютер временно переключен на текущий сервер:']
		for i in range(6):
			try:
				if i!=1:
					# message[i] = f'{message[i]} {self.get_status(five_bit_digit[5-i])}'
					message[i] = f'{self.get_status(five_bit_digit[5-i])}'
			except Exception as ex:
				print(ex)
				print(f'Err on {i} {five_bit_digit}')
		message.pop(1)
		# return '|'.join(message)
		# print(message)
		return message

	def get_status(self, bin_status):
		return True if bin_status==1 else False
