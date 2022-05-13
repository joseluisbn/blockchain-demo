import unittest
import json
from src.cryptocurrency import BlockChain, ComplexEncoder

class TestBlockChain(unittest.TestCase):
    def setUp(self):
        self.blockchain = BlockChain()

    def test_new_block(self):
        self.blockchain.new_block()
        self.assertEqual(len(self.blockchain.blocks), 1)
        self.assertEqual(self.blockchain.blocks[0].index, 0)
        self.assertEqual(self.blockchain.blocks[0].transactions, [])
        self.assertEqual(self.blockchain.blocks[0].previous_hash, None)

    def test_add_block(self):
        first_block = self.blockchain.new_block()
        second_block = self.blockchain.new_block()
        third_block = self.blockchain.new_block()
        self.assertEqual(self.blockchain.blocks[0].hash, first_block.hash)
        self.assertEqual(self.blockchain.blocks[1].hash, second_block.hash)
        self.assertEqual(self.blockchain.blocks[2].hash, third_block.hash)
        self.assertEqual(len(self.blockchain.blocks), 3)
        print(
            json.dumps(
                self.blockchain.repr_json(),
                cls=ComplexEncoder,
                sort_keys=True,
                indent=4,
            )
        )

    def test_keys(self):
        self.blockchain.generate_keys()

    def test_new_transaction(self):
        self.blockchain.new_transaction("Alice", "Bob", 100)
        self.assertEqual(len(self.blockchain.current_transactions), 1)
        self.assertEqual(self.blockchain.current_transactions[0].sender, "Alice")
        self.assertEqual(self.blockchain.current_transactions[0].receiver, "Bob")
        self.assertEqual(self.blockchain.current_transactions[0].amount, 100)
        self.blockchain.new_block()
        self.assertEqual(len(self.blockchain.current_transactions), 0)
        self.assertEqual(len(self.blockchain.blocks), 1)
        print(
            json.dumps(
                self.blockchain.repr_json(),
                cls=ComplexEncoder,
                sort_keys=True,
                indent=4,
            )
        )

    def test_p2p(self):
        blockchain1 = BlockChain("127.0.0.1", 60001)
        blockchain2 = BlockChain("127.0.0.1", 60002)

        blockchain1.register_node("127.0.0.1", 60002)
        blockchain2.register_node("127.0.0.1", 60001)

        blockchain1.new_transaction("Alice", "Bob", 100)
        blockchain1.new_transaction("Bob", "Alice", 20)
        blockchain1.new_block()

        blockchain2.perform_consensus()
        print(
            json.dumps(
                blockchain1.repr_json(), cls=ComplexEncoder, sort_keys=True, indent=4
            )
        )
        print(
            json.dumps(
                blockchain2.repr_json(), cls=ComplexEncoder, sort_keys=True, indent=4
            )
        )
if __name__ == "__main__":
    unittest.main()