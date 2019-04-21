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


class TestHDD(unittest.TestCase):

    def test_stress_hdd(self):
        self.assertEqual(stress_ng.stress_hdd(method="wr-seq",max_ops=1,hdd_bytes=10244444,instance=1),0)

        #stress_set_hdd_opts(method="wr-seq,sync")
        #stress_set_hdd_bytes(hdd_bytes=(1024*40000000))
        #stress_set_hdd_write_size(hdd_write_size=(65000))
        #c_args_t_p = build_args_t(counter=1,
        #         name="",
        #        max_ops=0,
        #         instance=1,
        #         num_instances=1,
        #         do_print=False)
        #print(_stress_ng.stress_hdd(c_args_t_p,do_c_print=True))

if __name__ == '__main__':
    unittest.main()
