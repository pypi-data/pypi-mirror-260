"""
    QMVC - Reference Implementation of paper: 
    
    "Mean Value Coordinates for Quad Cages in 3D", 
    jean-Marc Thiery, Pooran Memari and Tamy Boubekeur
    SIGGRAPH Asia 2018
    
    This program allows to compute QMVC for a set of 3D points contained 
    in a cage made of quad and triangles, as well as other flavors of 
    space coordinates for cages (MVC, SMVC, GC, MEC). It comes also with 
    a 3D viewer which helps deforming a mesh with a cage. 
    
    Copyright (C) 2018  jean-Marc Thiery, Pooran Memari and Tamy Boubekeur

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import math
import numpy as np

from .utils import *

def getAngleBetweenUnitVectors( u1 , u2 ):
    return 2.0 * math.asin( vecNorm(u1 - u2) * 0.5 )

"""
template< class int_t , class float_t , class point_t >
bool computeCoordinatesSimpleCode(
        point_t const & eta ,
        std::vector< std::vector< int_t > > const & cage_triangles ,
        std::vector< point_t > const & cage_vertices ,
        std::vector< point_t > const & cage_normals ,
        std::vector< float_t > & weights ,
        std::vector< float_t > & w_weights)
{
"""
def computeCoordinates(eta, cage_triangles, cage_vertices, cage_normals, weights):
    epsilon = 0.000000001
    cage_triangles = cage_triangles.astype(int)

    n_vertices = len(cage_vertices)
    n_triangles = len(cage_triangles)
    assert len(cage_normals) == len(cage_triangles), "cage_normals.size() != cage_triangles.size()"

    sumWeights = 0.0;

    d = np.zeros((n_vertices))      # distance between eta and each cage_vertices
    u = np.zeros((n_vertices, 3))   # direction vector from eta to each cage_vertices

    #d = np.linalg.norm(eta - cage_vertices, axis=1)
    #u = ( cage_vertices - eta ) / d

    for v in range(n_vertices):
        d[ v ] = vecNorm( eta - cage_vertices[ v ] )
        if d[ v ] < epsilon :
            weights[v] = 1.0
            return True
        u[ v ] = ( cage_vertices[v] - eta ) / d[v]

    #weights.fill(0.0)

    vid = np.zeros(3).astype(int)
    l = np.zeros(3)
    theta = np.zeros(3)
    w = np.zeros(3)

    pt = np.zeros((3, 3))
    ptDiff = np.zeros((3, 3))
    N = np.zeros((3, 3))
    invNorm2N = np.zeros(3)
    
    for t in range(n_triangles):
        # the Norm is CCW :

        vid = cage_triangles[t].copy()

        l[0] = vecNorm(u[vid[1]] - u[vid[2]])
        l[1] = vecNorm(u[vid[2]] - u[vid[0]])
        l[2] = vecNorm(u[vid[0]] - u[vid[1]])

        theta = 2.0 * np.arcsin(l * 0.5)

        """
        // test in original MVC paper: (they test if one angle psi is close to 0: it is "distance sensitive" in the sense that it does not
        // relate directly to the distance to the support plane of the triangle, and the more far away you go from the triangle, the worse it is)
        // In our experiments, it is actually not the good way to do it, as it increases significantly the errors we get in the computation of weights and derivatives,
        // especially when evaluating Hfx, Hfy, Hfz which can be of norm of the order of 10^3 instead of 0 (when specifying identity on the cage, see paper)

        // simple test we suggest:
        // the determinant of the basis is 2*area(T)*d( eta , support(T) ), we can directly test for the distance to support plane of the triangle to be minimum
        """
        determinant = vecDot( cage_vertices[vid[0]] - eta , vecCross( cage_vertices[vid[1]] - cage_vertices[vid[0]] , cage_vertices[vid[2]] - cage_vertices[vid[0]] ) )
        if determinant == 0:
            determinant = epsilon
        invDeterminant = 1.0 / determinant
        divVal = 4 * vecLenSqr(vecCross( cage_vertices[vid[1]] - cage_vertices[vid[0]] , cage_vertices[vid[2]] - cage_vertices[vid[0]] ))
        #sqrdist = 0.0
        #if divVal > 0:
        sqrdist = determinant*determinant / divVal
        dist = math.sqrt( sqrdist )

        if dist < epsilon :
            # then the point eta lies on the support plane of the triangle
            h = ( theta[0] + theta[1] + theta[2] ) / 2.0;
            if math.pi - h < epsilon:
                # eta lies inside the triangle t , use 2d barycentric coordinates :
                for i in range(3):
                    w[ i ] = math.sin( theta[ i ] ) * l[ (i+2) % 3 ] * l[ (i+1) % 3 ]

                sumWeights = w[0] + w[1] + w[2]

                #w_weights.fill(0.0)
                weights.fill(0.0)
                weights[ vid[0] ] = w[0] / sumWeights
                weights[ vid[1] ] = w[1] / sumWeights
                weights[ vid[2] ] = w[2] / sumWeights
                return True


        pt = cage_vertices[vid]

        ptDiff = pt - eta

        N[0] = vecCross( ptDiff[1] , ptDiff[2] )
        N[1] = vecCross( ptDiff[2] , ptDiff[0] )
        N[2] = vecCross( ptDiff[0] , ptDiff[1] )

        invNorm2N = 1.0 / (2.0 * np.linalg.norm(N, axis=1))

        for i in range(3):
            w[i] = 0.0
            for j in range(3):
                w[i] += theta[j] * vecDot( N[i] , N[j] ) * invNorm2N[j]
            w[i] *= invDeterminant

        sumWeights += ( w[0] + w[1] + w[2] )
        weights[ vid[0] ] += w[0]
        weights[ vid[1] ] += w[1]
        weights[ vid[2] ] += w[2]

    weights /= sumWeights

    return False

#"""
#template< class int_t , class float_t , class point_t >
#bool computeCoordinatesSimpleCode(
#        point_t const & eta ,
#        std::vector< std::vector< int_t > > const & cage_triangles ,
#        std::vector< point_t > const & cage_vertices ,
#        std::vector< point_t > const & cage_normals ,
#        std::vector< float_t > & weights)
#"""
#def computeCoordinatesSimpleCode(eta , cage_triangles , cage_vertices , cage_normals , weights):
#    w_weights = np.zeros((len(cage_vertices)))
#    return computeCoordinatesSimpleCodeWithWeights(eta , cage_triangles , cage_vertices , cage_normals , weights , w_weights );

#"""
#template< class int_t , class float_t , class point_t >
#bool computeCoordinates(
#        point_t const & eta ,
#        std::vector< std::vector< int_t > > const & cage_triangles ,
#        std::vector< point_t > const & cage_vertices ,
#        std::vector< point_t > const & cage_normals ,
#        std::vector< float_t > & weights ,
#        std::vector< float_t > & w_weights)// unnormalized weights
#"""
#def computeCoordinatesWithWeights(eta,cage_triangles,cage_vertices,cage_normals,weights,w_weights):
#    #return computeCoordinatesOriginalCode(eta,cage_triangles,cage_vertices,cage_normals,weights,w_weights);
#    return computeCoordinatesSimpleCodeWithWeights(eta,cage_triangles,cage_vertices,cage_normals,weights,w_weights);


#"""
#template< class int_t , class float_t , class point_t >
#bool computeCoordinates(
#        point_t const & eta ,
#        std::vector< std::vector< int_t > > const & cage_triangles ,
#        std::vector< point_t > const & cage_vertices ,
#        std::vector< point_t > const & cage_normals ,
#        std::vector< float_t > & weights)
#"""
#def computeCoordinates(eta,cage_triangles,cage_vertices,cage_normals,weights):
#    w_weights = np.zeros((len(cage_vertices)))
#    return computeCoordinatesWithWeights(eta,cage_triangles,cage_vertices,cage_normals,weights,w_weights)


"""
MVC : Code from "Mean Value Coordinates for Closed Triangular Meshes" Schaeffer Siggraph 2005
template< class int_t , class float_t , class point_t >
bool computeCoordinatesOriginalCode(
        point_t const & eta ,
        std::vector< std::vector< int_t > > const & cage_triangles , std::vector< point_t > const & cage_vertices , std::vector< point_t > const & cage_normals ,
        std::vector< float_t > & weights , std::vector< float_t > & w_weights)
{
"""
"""
def computeCoordinatesOriginalCode(eta, cage_triangles, cage_vertices, cage_normals, weights, w_weights):
    n_vertices = len(cage_vertices)
    n_triangles = len(cage_triangles)
    assert len(cage_normals) == len(cage_triangles), "cage_normals.size() != cage_triangles.size()"
    epsilon = 0.00000001;

    #w_weights.clear();
    #weights.clear();
    #weights.resize( n_vertices , 0.0 );
    sumWeights = 0.0;

    d = np.zeros((n_vertices))
    u = np.zeros((n_vertices, 3))

    for v in range(n_vertices):
        d[ v ] = vecNorm( eta - cage_vertices[ v ] );
        if( d[ v ] < epsilon ):
            weights[v] = 1.0
            return True
        u[ v ] = ( cage_vertices[v] - eta ) / d[v]

    w_weights.fill(0.0)

    vid = np.zeros(3)
    l = np.zeros(3)
    theta = np.zeros(3)
    w = np.zeros(3)
    c = np.zeros(3)
    s = np.zeros(3)
    
    for t in range(n_triangles): #the Norm is CCW :
        for i in range(2): vid[i] = cage_triangles[t][i].copy()
        for i in range(2): l[ i ] = vecNorm( u[ vid[ ( i + 1 ) % 3 ] ] - u[ vid[ ( i + 2 ) % 3 ] ] )
        for i in range(2): theta[i] = 2.0 * math.asin( l[i] / 2.0 );


        T h = ( theta[0] + theta[1] + theta[2] ) / 2.0;
        if( M_PI - h < epsilon ) { // eta is on the triangle t , use 2d barycentric coordinates :
            for( unsigned int i = 0 ; i <= 2 ; ++i ) w[ i ] = sin( theta[ i ] ) * l[ (i+2) % 3 ] * l[ (i+1) % 3 ];

            sumWeights = w[0] + w[1] + w[2];

            w_weights.clear();
            weights[ vid[0] ] = w[0] / sumWeights;
            weights[ vid[1] ] = w[1] / sumWeights;
            weights[ vid[2] ] = w[2] / sumWeights;
            return true;
        }

        for( unsigned int i = 0 ; i <= 2 ; ++i ) c[ i ] = ( 2.0 * sin(h) * sin(h - theta[ i ]) ) / ( sin(theta[ (i+1) % 3 ]) * sin(theta[ (i+2) % 3 ]) ) - 1.0;

        T sign_Basis_u0u1u2 = 1;
        if( point_t::dot( point_t::cross(u[vid[0]] , u[vid[1]]) , u[vid[2]] ) < 0.0 ) sign_Basis_u0u1u2 = -1;
        for( unsigned int i = 0 ; i <= 2 ; ++i ) s[ i ] = sign_Basis_u0u1u2 * sqrt( std::max<double>( 0.0 , 1.0 - c[ i ] * c[ i ] ) );
        if( fabs( s[0] ) < epsilon   ||   fabs( s[1] ) < epsilon   ||   fabs( s[2] ) < epsilon ) continue; // eta is on the same plane, outside t  ->  ignore triangle t :  
        for( unsigned int i = 0 ; i <= 2 ; ++i ) w[ i ] = ( theta[ i ] - c[ (i+1)% 3 ]*theta[ (i+2) % 3 ] - c[ (i+2) % 3 ]*theta[ (i+1) % 3 ] ) / ( 2.0 * d[ vid[i] ] * sin( theta[ (i+1) % 3 ] ) * s[ (i+2) % 3 ] );

        sumWeights += ( w[0] + w[1] + w[2] );
        w_weights[ vid[0] ] += w[0];
        w_weights[ vid[1] ] += w[1];
        w_weights[ vid[2] ] += w[2];
    }

    for( unsigned int v = 0 ; v < n_vertices ; ++v ) weights[v]  = w_weights[v] / sumWeights;

    return false;
}



template< class int_t , class float_t , class point_t >
bool computeCoordinatesOriginalCode(
        point_t const & eta ,
        std::vector< std::vector< int_t > > const & cage_triangles ,
        std::vector< point_t > const & cage_vertices ,
        std::vector< point_t > const & cage_normals ,
        std::vector< float_t > & weights)
{
    std::vector< float_t > w_weights;
    return computeCoordinatesOriginalCode(eta , cage_triangles , cage_vertices , cage_normals , weights , w_weights );
}
"""

def main(argv):
    """
    template< class int_t , class float_t , class point_t >
    bool computeCoordinates(
            point_t const & eta ,
            std::vector< std::vector< int_t > > const & cage_triangles ,
            std::vector< point_t > const & cage_vertices ,
            std::vector< point_t > const & cage_normals ,
            std::vector< float_t > & weights)
    """
    #eta = np.array([0.1, 0.5, 0.1])
    #cage_vertices = np.array([ \
    #    [0.0, 0.0, 0.0],\
    #    [1.0, 0.0, 0.0],\
    #    [0.0, 1.0, 0.0],\
    #    [0.0, 0.0, 1.0]\
    #])
    #cage_triangles = np.array([ \
    #    [0, 1, 2],\
    #    [2, 1, 3],\
    #    [0, 1, 3],\
    #    [0, 2, 3]\
    #])
    eta = np.array([1.0, 1.0, 0.5])
    cage_vertices = np.array([ \
        [0.0, 0.0, 0.0],\
        [1.0, 0.0, 0.0],\
        [1.0, 1.0, 0.0],\
        [0.0, 1.0, 0.0],\
        [0.0, 0.0, 1.0],\
        [1.0, 0.0, 1.0],\
        [1.0, 1.0, 1.0],\
        [0.0, 1.0, 1.0],\
    ])
    cage_triangles = np.array([ \
        [0, 1, 2],\
        [0, 2, 3],\
        [4, 6, 5],\
        [4, 7, 6],\
        [0, 4, 1],\
        [1, 4, 5],\
        [3, 7, 2],\
        [2, 7, 6],\
        [0, 7, 4],\
        [4, 7, 3],\
    ])
    cage_normals = []
    for t in range(len(cage_triangles)):
        p0 = cage_vertices[cage_triangles[t][0]].copy()
        p1 = cage_vertices[cage_triangles[t][1]].copy()
        p2 = cage_vertices[cage_triangles[t][2]].copy()
        cage_normals += [vecNormalized(vecCross(p1-p0, p2-p0))]
    cage_normals = np.array(cage_normals)
    weights = np.zeros((len(cage_vertices)))
    print(eta)
    print(computeCoordinates(eta,cage_triangles,cage_vertices,cage_normals,weights))
    print(weights)
    res = np.zeros(3)
    weightsSum = 0.0
    for i in range(len(cage_vertices)):
        res += cage_vertices[i] * weights[i]
        weightsSum += weights[i]
    print(res, weightsSum)


if __name__ == '__main__':
    import sys

    main(sys.argv)