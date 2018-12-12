import stress_ng, time, unittest 

class TestCPU(unittest.TestCase):

    def test_ms_sim_cpu_ackermann(self):
        self.assertEqual(stress_ng.ms_sim_stress_cpu(method="ackermann"),0)

    def test_ms_test_ms_sim_cpu_unknown(self):
        self.assertEqual(stress_ng.ms_sim_stress_cpu(method="unknown"),0)

    def test_ms_sim_cpu_ackermann_load_str_parm(self):
        self.assertEqual(stress_ng.ms_sim_stress_cpu(method="ackermann",load="10"),0)

    def test_ms_sim_cpu_ackermann_load_int_parm(self):
        self.assertEqual(stress_ng.ms_sim_stress_cpu(method="ackermann",load=10) ,0)


class TestVM(unittest.TestCase):

	def test_ms_sim_vm_zero_one(self):
		self.assertEqual(stress_ng.ms_sim_stress_vm(method="zero-one"),0)

	def test_ms_sim_vm_zero_onesss(self):
		self.assertEqual(stress_ng.ms_sim_stress_vm(method="zero-onesss"),0)

	def test_ms_sim_vm_zero_one_vm_bytes_str_1000000(self):
		self.assertEqual(stress_ng.ms_sim_stress_vm(method="zero-one",vm_bytes="10000000"),0)

	def test_ms_sim_vm_zero_one_vm_bytes_int_1000000(self):
		self.assertEqual(stress_ng.ms_sim_stress_vm(method="zero-one",vm_bytes=10000000),0)

if __name__ == '__main__':
    unittest.main()
