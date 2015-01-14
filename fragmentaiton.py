import rhinoscriptsyntax as rs
import math

def Fragmentation():
    surface_id = rs.GetObject("Select surface", rs.filter.surface)
    if surface_id is None: return

    rows = rs.GetInteger("Number of rows", 10, 3)
    if rows is None: return

    columns = rs.GetInteger("Number of columns", 10, 3)
    if columns is None: return

    uDomain = rs.SurfaceDomain(surface_id, 0)
    vDomain = rs.SurfaceDomain(surface_id, 1)
    if uDomain is None or vDomain is None: return

    for i in xrange(0,rows):
        stepU = (uDomain[1] - uDomain[0]) / (rows-1)
        paramU = uDomain[0] + (stepU * i)
        for j in xrange(0,columns):
            stepV = (vDomain[1] - vDomain[0]) / (columns-1)
            paramV = vDomain[0] + (stepV * j)

            vertices = SetTriangleVertices(surface_id, paramU, paramV, stepU, stepV)
            if vertices: rs.AddPolyline(vertices, None)

def SetTriangleVertices(surface_id, paramU, paramV, stepU, stepV):
    #vertice1
    pointScale = 0
    srfNormal = UnitizedSurfaceNormal(surface_id, [paramU, paramV])
    srfNormal = rs.VectorScale(srfNormal, pointScale)
    pointOnSrf = rs.EvaluateSurface(surface_id, paramU, paramV)
    vertice1 = rs.VectorAdd(pointOnSrf, srfNormal)

    #vertice2
    pointScale = 0
    srfNormal = UnitizedSurfaceNormal(surface_id, [paramU + stepU, paramV])
    srfNormal = rs.VectorScale(srfNormal, pointScale)
    pointOnSrf = rs.EvaluateSurface(surface_id, paramU + stepU , paramV)
    vertice2 = rs.VectorAdd(pointOnSrf, srfNormal)

    #vertice3
    pointScale = 0
    srfNormal = UnitizedSurfaceNormal(surface_id, [paramU, paramV + stepV])
    srfNormal = rs.VectorScale(srfNormal, pointScale)
    pointOnSrf = rs.EvaluateSurface(surface_id, paramU, paramV + stepV)
    vertice3 = rs.VectorAdd(pointOnSrf, srfNormal)

    return [vertice1, vertice2, vertice3, vertice1]

def UnitizedSurfaceNormal(srf, uvParams):
    srfNormal = rs.SurfaceNormal(srf, uvParams)
    return rs.VectorUnitize(srfNormal)

if __name__ == "__main__":
    Fragmentation()
