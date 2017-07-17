# paxos

声明：
1. 本文思路完成模仿 [朱一聪][1] 老师的的 [如何浅显易懂地解说 Paxos][2] 而得，版权属于  [朱一聪][3] 老师 。只是为了自己理解更加透彻，又重新推导了一下而已。文章发出已经获得 [朱一聪][4] 老师的同意。
2. 本文最后结论完全引用 [Paxos Made Simple][5] 中文翻译版
3. 学习 paxos 请优先选择 [Paxos Made Simple][6] 和 [Paxos lecture][7]，不要选择本文。本文仅能起到引导思路的作用
4. 文章肯定有不严谨，推导不严谨的地方，欢迎讨论。

### 背景：

在一个高可用分布式存储系统中，如果只使用一台机器，只要这台机器故障，系统就会崩溃。所以肯定需要多台机器，但是由于网络延迟，机器崩溃等原因，多台机器对于数据很难达成共识（Consensus not Consistency）。而 paxos 协议就是用来使各个机器达成共识的协议。

### 如何理解共识（Consensus）：
共识就是在一个或多个进程提议了一个值应当是什么后，使系统中所有进程对这个值达成一致意见。但是必须明确：在一个完全异步且可能出现任何故障的系统中，不存在一个算法可以确保达到共识（[FLP Impossibility][8]）。

### 前提:
#### 需要保证安全性：
 1. 只有被提出的提案才能被选定 
 2. 只能有一个值被选定
 3. 如果某个进程认为某个提案被选定了，那么这个提案必须是真的被选定的那个
#### 可能出现的场景
 1. 进程之间的通信可能出现故障
 2. 每个进程都可能提出不同的值
 3. 每个进程也可能随时崩溃
 4. 进程之间传输的数据不会篡改
#### 达成共识的条件
N 个进程中大多数（超过一半）进程都选定了同一个值

### 推导流程
假设存在三个进程 p1 p2 p3，共同决定 v 的值
#### 1.1 每个进程只接受收到的第一个提案
##### 场景 1.1.1
p1 proposal：v = a 
p2 proposal: v = b 
p3 proposal: 无

假设是 p1 的 proposal 优先到达 p3，p2 的 proposal 在到达 p3 时会被拒绝，系统就 v = a 达成了共识，反之如果 p2 的 proposal 优先到达，系统会就 v = b 达成共识。

##### 场景 1.1.2
p1 proposal：v = a 
p2 proposal: v = b 
p3 proposal: v = c

这样每个机器只能接受自己机器上的 proposal，对于 v 的值就永远不能达成共识了。

##### 结论 1.1： 
 1. 进程必须能够多次改写 v 的值，否则可能永远达不成共识
 2. 进程必须接受第一个 proposal，否则可能永远达不成共识（系统只有一个提案时）

#### 1.2 每个进程只接受 proposal_id 大的提案
根据 1.1 的结论，进程必须接受第一个 proposal， 所以需要一种拒绝策略或者修正后到达的 proposal 的 value 我们需要额外的信息作为依据来完成。
1. 我们得到哪些信息呢？
提出 proposal 进程的标识 process_id，当前进行到轮次 round_number（每个进程自增）
2. 这些信息有什么用？
这两个信息加在一起标识唯一的 proposal
暂定 proposal_id = round_number + process_id
3. 如何更新 proposal_id？
每个 process 的 proposal_id = max(proposal_id, a_proposal_id)


##### 场景 1.2.1 
假设 p1_proposal_id > p2_proposal_id
p1 proposal：v = a 
p2 proposal: v = b 
p3 proposal: 无

如果 p1 proposal 先到达 p3 ，p2 后到达，会形成
p1 proposal：v = a 
p2 proposal: v = a
p3 proposal: v = a 
系统就 v = a 达成共识。

##### 场景 1.2.2
如果 p2 proposal 先到达 p3 , p1 后到达，p3 会先接受 p2 proposal，形成
p1 proposal：v = a 
p2 proposal: v = b
p3 proposal: v = b
系统就 v = b 达成共识，因为 p1 proposal 也已经发出，接着又会形成
p1 proposal：v = a 
p2 proposal: v = a
p3 proposal: v = a
系统又就 v = a 达成了共识。
在这个策略中，有两个值先后达成共识，不满足安全性。
##### 结论 1.2：
按照现有 1.2 策略存在proposal id 小 proposal 先到达，系统多次就不同的值达成共识的问题。从如下几个角度思考解决此问题
   1. p3 可以拒绝 p2 proposal(p2 proposal 先到达 p3，p2_proposal_id < p1_proposal_id )
   2. 限制 p1 提出的 proposal
    
#### 1.3 p3 可以拒绝 p2 proposal 角度
1.  发送带有 proposal_id  PreProposal,
2.  接收到 PreProposal 的进程，根据 proposal_id = max(proposal_id, accept_proposal_id) 进行更新
3.  进程发送 proposal 
4.  每个进程只接受 proposal_id 大的 proposal

假设 p1_proposal_id > p2_proposal_id
p1 proposal：v = a 
p2 proposal: v = b 
p3 proposal: 无

##### 场景 1.3.1 
1. p1_PreProposal 携带 p1_proposal_id 到达 p3
2. P3 更新 p3_proposal_id 为 p1_proposal_id,  P2 更新 p2_proposal_id 为 p1_proposal_id
3. p2_PreProposal 携带 p2_proposal_id 到达，p2_proposal_id < p1_proposal_id，被拒绝。
4. p1_proposal (v = a)到达 p2, p3
5. 此时系统就 v = a 达成共识
    - p1: v = a
    - p2: v = a
    - p3: v = a

##### 场景 1.3.2
1. p2_PreProposal 携带 p2_proposal_id 进行广播，到达 p3
2. P3 更新 p3_proposal_id 为 p2_proposal_id
3. p2_proposal (v = b)到达 p3，系统此时会就 v = b 达成共识
    - p1: v = a
    - p2: v = b
    - p3: v = b
4. p1_PreProposal 携带 p1_proposal_id 进行广播，到达 p2, p3, p2_proposal_id < p1_proposal_id，p2 p3 更新 proposal_id 为 p1_proposal_id
5. p1_proposal (v = a)到达 p2, p3
6. 此时系统就 v = a 达成共识
    - p1: v = a
    - p2: v = a
    - p3: v = a
##### 结论 1.3:
1.3 策略解决了一部分问题，但是还是依赖消息到达的先后顺序。在某些条件下还是不能保证安全性。

#### 1.4 限制 p1 提出的 proposal
现在已知 process_id round_number，还能得到哪些信息？
按照 1.3 的策略，我们只是更新了接受 pre_proposal 的 accept_process 的 proposal_id 为较大的 proposal_id，并没有回复给发送 pre_propoal 的 send_process 任何消息。是不是可以把 accept_process 已经获得的提案的 proposal_id 和 proposal 这样是不是限制 send_process 接下来发送的 proposal ？现在模拟一下流程，看看能否解决 1.3 中存在的问题。

1.  发送带有 proposal_id 的 PreProposal
2.  接收到 PreProposal 的进程，根据 proposal_id = max(proposal_id, accept_proposal_id) 进行更新，并回复当前进程已经接收到的 proposal_id
3.  进程发送 proposal 
4.  每个进程只接受 proposal_id 大的 proposal
假设 p1_proposal_id > p2_proposal_id
p1 proposal：v = a 
p2 proposal: v = b 
p3 proposal: 无

##### 场景 1.4.1
1. p2_PreProposal 携带 p2_proposal_id 进行广播，到达 p3
2. P3 更新 p3_proposal_id 为 p2_proposal_id
3. P3 给 P2回复 (p2_proposal_id, v=NULL)
3. p2_proposal (v = b)到达 p3，系统此时会就 v = b 达成共识
    - p1: v = a
    - p2: v = b
    - p3: v = b
4. p1_PreProposal 携带 p1_proposal_id 进行广播，到达 p2, p3, p2_proposal_id < p1_proposal_id，p2 p3 更新 proposal_id 为 p1_proposal_id
5. P3 回复 P1 (p2_proposal_id, v=b)
6. P1 发现 P3 已经接受了 v = b，把自己的提案 v = a 修改成 v = b
5. p1_proposal (v = b)到达 p2, p3
6. 此时系统还是就 v = b 达成共识
    - p1: v = b
    - p2: v = b
    - p3: v = b
问题得到了解决。
上文所有的推导，全部来源于三个进程，看似问题已经解决。但是这个流程能否一般化，应用于 N 个进程呢？提案数从 2 到 N 呢？

#### 泛化推导，

##### 场景 1.5 进程数从 3 到 N
Pi 进程集合：提出 PreProposal-i，Proposal-i(v = a)
Qi 进程集合：接受了 Proposal-i 的超半数进程
Pj 进程集合：提出 PreProposal-j，Proposal-j(v = b)
Qj 进程集合：接受了 Proposal-j 的超半数进程
Pk 进程集合：Qi 和 Qj 的进程集合交集
只要 Pk 能够拒绝 Proposal-i 和 Proposal-j 的一个就是安全的

每个 Proposal-j-id < Proposal-i-id
1. Proposal-j 到达部分进程，此时系统未达成共识
2. PreProposal-i 到达部分进程，此时系统未达成共识
3. 所有接收到 PreProposal-i 的进程回复（Proposal-j-id， v = b）或者 （NULL， NULL） 给 Pi
4. Pi 接受到（Proposal-j-id，v = b），将 Proposal-i 原先的 v = a 修改成 v = b，然后进行广播。
5. 系统就 v = b 达成共识。

##### 场景 1.6 不同的 proposal 由 2 到 N
假设 j - i = N，b - a = N
Pi Pi+1 ... Pi+N-1 Pj 每个进程组都会提出 Proposal(v = a, a+1, .. a+N-1, b) Proposal_id 大小顺序相反
Qi -> Qj 与 Pi 相对
Pk 是收到了很多不同提案的进程的集合，但是一直没有达成共识。

1. Proposal-i+1 Proposal-i+2 到达 Pk，系统并没有达成共识。
2. PreProposal-j 发出到达部分进程 
3. 接收到 PreProposal-j 的进程选择 [(Proposal-i+1-id, v = a + 1), (Proposal-i+2-id, v = a + 2)] 其中的一个或者两个一起回复给 Pj
4. Pj 应该选择哪个 v 值修改自己的 proposal 呢
    - 回顾前边的逻辑，每个进程会拒绝 Proposal-id 较小的提案，Proposal-i+1-id > Proposal-i+2-id
    - Proposal-i+1-id 相比 Proposal-i+2-id 的提案肯定先到 Pk 的，系统还有一部分进程没有接收到 (Proposal-i+1-id, v = a + 1)，没有就 (Proposal-i+1-id, v = a + 1) 形成共识
    -  假设 Pj 选择 proposal_id 较小的 proposal ，那么会选择  （Proposal-i+2-id, v = a + 2) ，在 Pj 发出 （Proposal-j, v = a + 2) 之前，没有收到 (Proposal-i+1-id, v = a + 1) 的进程可能恰好收到了，系统就 v = a + 1 达成了共识。此后（Proposal-j, v = a + 2) 达到了， 系统又 v = a + 2 达成的共识。系统两次达成共识，存在问题。
    -  假设 Pj 选择 proposal_id 较大的 proposal，那么会选择  （Proposal-i+1-id, v = a + 1) ，在 Pj 发出 （Proposal-j, v = a + 1) 之前，没有收到 (Proposal-i+1-id, v = a + 1) 的进程可能恰好收到了，系统就 v = a + 1 达成了共识。此后（Proposal-j, v = a + 2) 达到了，还是 v = a + 1。不存在问题。
    -   系统选择 proposal_id 较大的修改依据
5. Pj 选择 proposal_id 较大的 proposal，修改 v = a + 1，并发出 （Proposal-j, v = a + 2）
6. 系统就 v = a + 2 达成共识

#### 不能覆盖的场景
如果每次 proposal 被接受之前，先接受了携带较大 proposal-id 的 PreProposal，这样每次都会拒绝即将成功的达成共识的 proposal 系统每次都不会达成共识。这个场景可以通过不断重试解决。

#### paxos
Proposer： 发起提案的进程
Acceptor： 接受题提案的进程
一个进程可能充当多个角色
##### Phase 1:
1. Proposer 选择一个提案编号 n，然后向 Acceptors 的某个 majority 集合的成员发送编号为 n 的prepare请求。
2. 如果一个Acceptor收到一个编号为 n 的prepare请求，且 n 大于它已经响应的所有prepare请求的编号，那么它就会保证不会再通过(accept)任何编号小于 n 的提案，同时将它已经通过的最大编号的提案(如果存在的话)作为响应。 

##### Phase 2
1. 如果 Proposer 收到来自半数以上的 Acceptor 对于它的 prepare 请求(编号为 n)的响应，那么它就会发送一个针对编号为 n ，value 值为 v 的提案的 accept 请求给 Acceptors，在这里 v 是收到的响应中编号最大的提案的值，如果响应中不包含提案，那么它就是任意值。
2. 如果 Acceptor 收到一个针对编号 n 的提案的accept请求，只要它还未对编号大于 n 的 prepare 请求作出响应，它就可以通过这个提案。

            














 
 


  [1]: https://www.zhihu.com/people/zhu-yicong/answers
  [2]: https://www.zhihu.com/question/19787937/answer/82340987
  [3]: https://www.zhihu.com/people/zhu-yicong/answers
  [4]: https://www.zhihu.com/people/zhu-yicong/answers
  [5]: http://dsdoc.net/paxosmadesimple/index.html
  [6]: http://lamport.azurewebsites.net/pubs/paxos-simple.pdf
  [7]: https://www.youtube.com/watch?v=JEpsBg0AO6o
  [8]: http://the-paper-trail.org/blog/a-brief-tour-of-flp-impossibility/
