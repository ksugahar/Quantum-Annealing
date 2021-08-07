######	標準ライブラリの読み込み
import sys, numpy, random

######	Factorization Machinesのライブラリの読み込み
from pyfm import pylibfm
from sklearn.feature_extraction import DictVectorizer

######	QUBOのライブラリの読み込み
from pyqubo import Binary, Constraint
from dimod import ExactSolver

######	C言語で作成した独自ハミルトニアン
import Hamiltonian



######	独自ハミルトニアンを利用したトレーニングデータの作成
train = []
targets = []
for n in range(2**12):
	sigma = [random.randint(0,1) for m in range(8)]
	energy = Hamiltonian.energy(sigma)
	sample = dict(zip(['s0','s1','s2','s3','s4','s5','s6','s7'],sigma))
	train.append(sample)
	targets.append((energy+300)/100000)

######	Factorization Machinesライブラリを用いた学習
v = DictVectorizer()
X = v.fit_transform(train)
fm = pylibfm.FM(num_factors=12, num_iter=300, verbose=False, task="regression", initial_learning_rate=0.001, learning_rate_schedule="optimal", k0=True, seed=0)
fm.fit(X,targets)

######	Factorization Machines学習結果からW行列とV行列を抽出
W = fm.w
V = numpy.zeros((8,8),dtype=float)
for i in range(8):
	for j in range(i+1,8):
		for k in range(fm.num_factors):
			V[i,j] = V[i,j] + fm.v[k,i]*fm.v[k,j]

######	W行列とV行列からQUBOモデルを構築
import pyqubo
s = 8*[0]
for n in range(8):
	s[n] = Binary("s%d" % n)
s = pyqubo.Array(s)
H = W.dot(s) + s.dot(V.dot(s))+fm.w0
model = H.compile()

######	トレーニングデータとFMモデルとQUBOモデルの結果のvalidation
for n in range(30):
	CF = fm.predict(v.transform(train[n]))
	QB =  model.energy(train[n],'BINARY')
	print('%.5f	%.5f	%.5f' % (targets[n],CF[0],QB-CF[0]))

######	QUBOモデルを古典計算機で最適化

bqm = model.to_bqm()
sampleset = ExactSolver().sample(bqm)
decoded_samples = model.decode_sampleset(sampleset)
best_sample = min(decoded_samples, key=lambda s: s.energy)
print(best_sample.energy)
print(best_sample.sample)

######	最適化結果を元のハミルトニアンで評価
energy = Hamiltonian.energy(list(best_sample.sample.values()))
print('%.5f' % (energy))

