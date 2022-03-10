import datetime
import hashlib
import json
from flask import Flask, jsonify

print('hola')

class Blockchain:
  def __init__(self) -> None:
      self.chain = []
      self.create_block(proof = 1, previous_hash = '0')

  def create_block(self, proof, previous_hash):
    block = {
      'index': len(self.chain) + 1,
      'timestamp': str(datetime.datetime.now()),
      'proof': proof,
      'previous_hash': previous_hash
    }
    self.chain.append(block)
    return block

  def get_previous_block(self):
    return self.chain[-1]

  def proof_of_work(self, previous_proof):
    new_proof = 1
    check_proof = False

    while check_proof is False:
      hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
      if hash_operation[:4] == '0000':
        check_proof = True
      else:
        new_proof += 1
    
    return new_proof

  def hash(self, block):
    encoded_block = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(encoded_block).hexdigest()

  def is_chain_valid(self, chain):
    previous_block = chain[0]
    block_index = 1
    while block_index < len(chain):
      # Validamos si es hash conside con el has del bloque anterior
      current_block = chain[block_index]
      if current_block['previous_hash'] != self.hash(previous_block):
        return False
      
      # Validamos si la prueba de trabajo es correcta
      previous_proof = previous_block['proof']
      current_proof = current_block['proof']
      hash_operation = hashlib.sha256(str(current_proof**2 - previous_proof**2).encode()).hexdigest()
      if hash_operation[:4] != '0000':
        return False

      # Validamos el segiuente bloque
      previous_block = current_block
      block_index += 1
    
    return True # Retornamos true indicando que la cadena es valida


#Crear app web
app = Flask(__name__)

blockchain = Blockchain()

# Minar un bloque
@app.route('/mine-block', methods=['GET'])
def mine_block():
  previous_block = blockchain.get_previous_block()
  proof = blockchain.proof_of_work(previous_block['proof'])
  block_created = blockchain.create_block(proof, blockchain.hash(previous_block))
  response = {
    'message': 'Haz minado un nuevo bloque!',
    'block': block_created
  }
  return jsonify(response), 200

# Obtener toda la cadena
@app.route('/get-chain', methods=['GET'])
def get_chain():
  response = {
    'chain': blockchain.chain,
    'length': len(blockchain.chain)
  }
  return jsonify(response), 200

@app.route('/is-chain-valid', methods=['GET'])
def is_chain_valid():
  chain = blockchain.chain
  is_valid = blockchain.is_chain_valid(chain)
  response = {
    'is_valid': is_valid
  }
  return jsonify(response), 200

app.run(host='0.0.0.0', port=5000)
