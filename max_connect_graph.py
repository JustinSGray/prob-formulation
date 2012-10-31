import networkx as nx
import matplotlib.pyplot as plt
import set_ops as so
import numpy
import pylab
import itertools
import edmonds

def cab(DG,s,m,n,w,p,pos):
	# this function creates the nodes and edges associated with an analysis block
    # sample input: cab(DG,'A',1,1,5,(2,3),pos);
    # DG = given directed graph
    # s = name of analysis block
    # m = number of local inputs
    # n = number of local outputs
    # w = cost of analysis
    # p = position for plotting
    # pos = dictionary for plotting
    #DG.graph['analyses'].append(s)
    local_inputs = []
    local_outputs = []
    si=s+'i'
    so = s+'o'
    DG.add_node(si,type='analysis_start',analysis_block=s)
    DG.add_node(so,type='analysis_finish',analysis_block=s)
    pos.update({si:numpy.array([p[0]-0.1,p[1]]),
                so:numpy.array([p[0]+0.1,p[1]]),
                s:numpy.array([p[0],p[1]])})
    DG.add_weighted_edges_from([(si,so,w)],type='analysis')
    x = numpy.arange(1,m+1) # local inputs
    y = numpy.arange(1,n+1) # local outputs
    for j in x:
        DG.add_node(si+str(j),type='local_input',analysis_block=s);
        local_inputs.append(si+str(j))
        if m>1:
            pos.update({si+str(j):numpy.array([p[0]-0.27,p[1]+0.2-0.4/(m-1)*(j-1)])})
        else:
            pos.update({si+str(j):numpy.array([p[0]-0.27,p[1]])})
        DG.add_weighted_edges_from([(si+str(j),si,0)],type='in')
    for j in y:
        DG.add_node(so+str(j),type='local_output',analysis_block=s);
        local_outputs.append(so+str(j))
        if n>1:
            pos.update({so+str(j):numpy.array([p[0]+0.25,p[1]+0.2-0.4/(n-1)*(j-1)])})
        else:
            pos.update({so+str(j):numpy.array([p[0]+0.25,p[1]])})
        DG.add_weighted_edges_from([(so,so+str(j),0)],type='out')
    nodes = {'local_inputs':local_inputs,'analysis_start':[si],'analysis_finish':[so],'local_outputs':local_outputs}
    DG.graph['analyses'][s]=nodes
    return;

def create_sample_graph():
	# Build the sample graph. Treat x as the root of all inputs without loss of generality.
	pos=dict() # for plotting

	w=0;
	DG=nx.DiGraph(type='maximal_connectivity',analyses=dict())
	DG.add_nodes_from(['x'],type='global_input',analysis_block='')
	DG.add_nodes_from(['y1','y2','y3','y4'],type='global_output',analysis_block='')
	pos.update({'x':numpy.array([1,2.5]),
				'y1':numpy.array([5,4]),
				'y2':numpy.array([5,3]),
				'y3':numpy.array([5,2]),
				'y4':numpy.array([5,1]),
				'y':numpy.array([6,3])})

	cab(DG,'A',2,2,1,(2,4),pos);
	a='x';
	b='Ai1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Ao1';
	b='Ei1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Ao1';
	b='Fi1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Ao2';
	b='Ei2';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')

	cab(DG,'B',1,2,1,(2,3),pos)
	a='x';
	b='Bi1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Bo1';
	b='Fi2';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Bo2';
	b='Gi1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')

	cab(DG,'C',1,1,1,(2,2),pos)
	a='x';
	b='Ci1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Co1';
	b='Gi1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Co1';
	b='Hi1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')

	cab(DG,'D',3,1,1,(2,1),pos)
	a='x';
	b='Di1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Do1';
	b='Gi2';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Do1';
	b='Hi2';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')

	cab(DG,'E',2,2,1,(3,4),pos)
	a='Eo1';
	b='Ii1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Eo2';
	b='Ji1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')

	cab(DG,'F',2,3,1,(3,3),pos)
	a='Fo1';
	b='Ii2';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Fo1';
	b='Ji1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Fo1';
	b='Ki1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')

	cab(DG,'G',2,2,1,(3,2),pos)
	a='Go1';
	b='Ji1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Go1';
	b='Li1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')

	cab(DG,'H',2,3,1,(3,1),pos)
	a='Ho1';
	b='Li2';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Ho1';
	b='Ki1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')

	cab(DG,'I',2,2,1,(4,4),pos)
	a='Io1';
	b='y1';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')

	cab(DG,'J',3,1,1,(4,3),pos)
	a='Jo1';
	b='y2';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')

	cab(DG,'K',3,2,1,(4,2),pos)
	a='Ko1';
	b='y3';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')

	cab(DG,'L',2,2,1,(4,1),pos)
	a='Lo1';
	b='y3';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	a='Lo2';
	b='y4';
	DG.add_weighted_edges_from([(a,b,w)],type='connection')
	
	# add a few more connections
	DG.add_weighted_edges_from([('Io2','Ai2',w),
        ('Ao1','Hi1',w),
		('Fo2','Gi2',w),
		('Ko2','y1',w),
		('Ho3','Di3',w),
		('Co1','Ai2',w),
		('Fo3','Di2',w),
		('Io2','Ki2',w),
        ('Ho2','y2',w),
		('Do1','Ji2',w)],
		type='connection')
	return[DG,pos];

def dict2tree(Gx,DG1,DG2):
	# this function converts a tree in dictionary form to networkx graph form
    DG2.add_nodes_from(DG1.nodes())
    nds=Gx.keys()
    vls=Gx.values()
    j=0
    for i in nds:
        if len(vls[j])>1:
            nd=vls[j][-2]
            DG2.add_weighted_edges_from([(nd,i,DG1[nd][i]['weight'])])
        j+=1
    return DG2;

def tree2path(G,root,node):
	# this function returns the path along a tree to the specified node
    Gtree = nx.DiGraph()
    Gtree.add_nodes_from(G.nodes())
    nodes = [node]
    cnode = node
    reached_root = False
    j = 1
    while j < 2*len(G.nodes()):
        j += 1
        k = False
        for i in G.edges():
            if i[1]== cnode:
                cnode = i[0]
                nodes.append(cnode)
                Gtree.add_edge(i[0],i[1],G[i[0]][i[1]])
                k = True
                break
        if cnode == root:
            k = False
            reached_root = True
        if k == False:
            break
    return [nodes,reached_root,Gtree];

def minimum_spanning_directed_graph(DG,root,outs):
	# this function exaustively finds the tree with the least weight that reaches the specified outputs
    # DG = maximal connectivity graph
    # root = root of the inputs
    # outs = desired outputs
    
    # Build a list of the edges that have nonzero weighting
    analysis_edges = []
    for i in DG.edges():
        w = DG[i[0]][i[1]]['weight']
        if w != 0:
            analysis_edges.append(i)

    DG0 = nx.DiGraph()
    DG0.add_nodes_from(DG.nodes())
    DGs = []
    weights = []
    print 'analysis edges',analysis_edges
    for x in itertools.product([0,1],repeat=len(analysis_edges)):
        DG0.add_edges_from(DG.edges())
        j = 0
        for i in x:
            if i == 0:
                DG0.remove_edge(analysis_edges[j][0],analysis_edges[j][1])
            j += 1
        Gx=nx.single_source_dijkstra_path(DG0,root)
        DG1=nx.DiGraph()
        DG1=dict2tree(Gx,DG,DG1)
        outcheck = [] ################ I also need to check to make sure all needed intermediate inputs are given
        req_ins = []
        for i in analysis_edges:
            if x[analysis_edges.index(i)] == 0:
                continue
            pds = DG.predecessors(i[0])
            for ii in pds:
                req_ins.append(ii)
        for i in outs+req_ins:
            out = tree2path(DG1,root,i)
            outcheck.append(out[1])
        if all(outcheck):
            total_graph_weight=0
            for e in DG1.edges(data=True):
                total_graph_weight=total_graph_weight+e[2]['weight'] #  e =[1,2,{weight=3.5}]
            weights.append(total_graph_weight)
            DGs.append(DG1)

    if len(weights) == 0:
        print 'no possible connecting tree'
        least_weight = []
        least_weight_graph = []
    else:
        least_weight = min(weights)
        least_weight_graph = DGs[weights.index(least_weight)]
##        # remove unused edges
##        k = 0
##        K = True
##        while K:
##            for i in least_weight_graph.edges():
##                print i
##                if i[1] in outs:
##                    continue
##                srs = least_weight_graph.successors(i[1])
##                print srs
##                if len(srs) == 0:
##                    print 'removed',i
##                    least_weight_graph.remove_edge(i[0],i[1])
##                    continue
##                K = False # exit while loop if there are no more edges to remove
##            if k > len(DG.nodes())**2:
##                break
##            k += 1
    return [least_weight,least_weight_graph];

def dgraph2dict(DG):
	DGdict = dict();
	nds = DG.nodes();
	for i in nds:
		x = dict();
		nghs = DG.neighbors(i)
		if len(nghs) == 0:
			continue
		for j in nghs:
			x[j] = DG[i][j]['weight']
		DGdict[i] = x
	return DGdict
	
def dict2dgraph(DGdict):
	DG = nx.DiGraph()
	for i in DGdict:
		DG.add_node(i)
		for j in DGdict[i]:
			DG.add_node(j)
			DG.add_edge(i,j,weight = DGdict[i][j])
	return DG

def edmonds_mst(root,DG):
	# minimum spanning tree using Edmonds algorithm (downloaded from 
	# https://github.com/mlbright/edmonds/tree/master/edmonds)
	# DG = directed graph
	# root = of the desired minimum spanning tree
	DGdict = dgraph2dict(DG)
	g = edmonds.mst(root,DGdict)
	h = dict2dgraph(g)
	return h;

def remove_node(DG,i):
    analysis = DG.node[i]['analysis_block']
    DG.remove_nodes_from(DG.graph['analyses'][analysis]['local_inputs'])
    DG.remove_nodes_from(DG.graph['analyses'][analysis]['local_outputs'])
    DG.remove_nodes_from(DG.graph['analyses'][analysis]['analysis_start'])
    DG.remove_nodes_from(DG.graph['analyses'][analysis]['analysis_finish'])
    del DG.graph['analyses'][analysis]
    return DG;
    
def obtain_fpf(maxDG):
    DG = maxDG.copy()
    
    # -- find and remove any holes (must iterate)
    check = True
    while check:
        nodes = DG.nodes()
        holes = []
        for i in nodes:
            if DG.node[i]['type']=='local_input':
                ins = DG.in_edges(i)
                if len(ins)==0:
                    holes.append(i)
        if len(holes)==0:
            check = False
        for i in holes:
            DG = remove_node(DG,i)
    
    # -- find and remove any conflicts
    nodes = DG.nodes()
    for i in nodes:
        if DG.node[i]['type']=='local_input':
            ins = DG.in_edges(i)
            if len(ins)>1:
                #ins.reverse()
                ins.remove(ins[0])
                DG.remove_edges_from(ins)
    
    # -- delete any analyses with no used inputs (must iterate)
    check = True
    while check:
        extraneous = []
        analyses = DG.graph['analyses']
        for i in analyses:
            outs = analyses[i]['local_outputs']
            j = 0
            for k in outs:
                j = j+len(DG.successors(k))
            if j==0:
                extraneous.append(k)
        if len(extraneous)==0:
            check = False
        for k in extraneous:
            DG = remove_node(DG,k)
    return DG;

def extract_simple_graph(DG):
    SG = nx.DiGraph()

    # add nodes
    nodes = DG.nodes()
    for i in nodes:
        if DG.node[i]['type']=='global_input':
            SG.add_node(i,type='global_input')
        if DG.node[i]['type']=='global_output':
            SG.add_node(i,type='global_output')
        if DG.node[i]['type']=='analysis_start':
            node = DG.node[i]['analysis_block']
            SG.add_node(node,type='analysis_block')
    
    # add edges
    edges = DG.edges()
    for i in edges:
        if DG.edge[i[0]][i[1]]['type']=='connection':
            type1 = DG.node[i[0]]['type']
            type2 = DG.node[i[1]]['type']
            if type1=='local_output':
                node1 = DG.node[i[0]]['analysis_block']
            else:
                node1 = i[0]
            if type2=='local_input':
                node2 = DG.node[i[1]]['analysis_block']
            else:
                node2 = i[1]
            SG.add_edge(node1,node2)
    return SG;

def find_cycles(DG):
    CG = nx.DiGraph()
    CG.add_nodes_from(DG.nodes())
    cycles = nx.simple_cycles(DG)
    for i in cycles:
        L = range(0,len(i)-1)
        for j in L:
            CG.add_edge(i[j],i[j+1])
    return [CG,cycles];

out = create_sample_graph()
maxDG = out[0]
pos = out[1]

FPF = obtain_fpf(maxDG)

SG = extract_simple_graph(maxDG)

out = find_cycles(SG) 
CGSG = out[0]
cyclesSG = out[1]
print cyclesSG
print CGSG.edges()

out = find_cycles(FPF) 
CG = out[0]
cycles = out[1]
#print len(cycles)
#print cycles

pylab.figure(1)
#nx.draw(maxDG,pos,width=3)
#nx.draw(FPF,pos,width=1.5,edge_color='b')
#nx.draw_networkx_edges(CG,pos,width=0.75,edge_color='y')
nx.draw(SG,pos,width=2)
nx.draw_networkx_edges(CGSG,pos,width=0.75,edge_color='y')

pylab.show()