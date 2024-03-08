
import numpy


class Quaternion :

    def __init__ ( self, s=1.0, v=(0,0,0) ) :
        self.s = s
        self.v = numpy.array(v, numpy.float32)

    def length (self) :
        vx,vy,vz = self.v
        return numpy.sqrt ( (self.s*self.s) + (vx*vx + vy*vy + vz*vz) )


    def rotation (self, angDegrees, axis) :
        angRad = 0.5 * angDegrees * numpy.pi / 180.0
        self.s = numpy.cos ( angRad )
        self.v = axis * numpy.sin ( angRad )


    def inverse ( self ) :
        return Quaternion ( self.s, self.v * -1.0 )


    def fromXform ( self, xf ) :
        axis, angle = xf.rotation_axis_and_angle ()
        angle_deg = (180 / numpy.pi) * angle
        self.rotation ( angle_deg, axis )

    def dot ( self, q ) :
        vx,vy,vz = self.v
        qvx, qvy, qvz = q.v
        return self.s * q.s + vx*qvx + vy+qvy + vz*qvz

    def angleTo ( self, q2 ) :
        self.normalize()
        q2.normalize()
        ca = self * q2
        if ca > 1:
            ca = 1
        elif ca < -1:
            ca = -1
        a = 2.0 * numpy.arccos ( ca )
        return a


    def normalize (self) :
        l = self.length()
        if (l > 1e-4) :
            self.s = self.s / l
            self.v = self.v / l
        else :
            raise ("quaternion normalization error")

    def __mul__(self, x) :
        if type(x) == type(1.0) :
            return Quaternion ( self.s*x, self.v*x )
        else :
            return self.dot ( x )

    def __add__(self, x) :
        return Quaternion ( self.s + x.s, self.v + x.v )

    def __sub__(self, x) :
        return Quaternion ( self.s - x.s, self.v - x.v )

    def __copy__ (self) :
        return Quaternion ( self.s, self.v )

    def Xform (self) :
        #self.normalize()
        s = self.s
        vx,vy,vz = self.v
        from chimerax.geometry import Place
        return Place (
            [(1-2*vy*vy-2*vz*vz, 2*vx*vy-2*s*vz, 2*vx*vz+2*s*vy, 0),
             (2*vx*vy+2*s*vz, 1-2*vx*vx-2*vz*vz, 2*vy*vz-2*s*vx, 0),
             (2*vx*vz-2*s*vy, 2*vy*vz+2*s*vx, 1-2*vx*vx-2*vy*vy, 0)]
        )

    def matrix (self) :
        #self.normalize()
        s = self.s
        vx,vy,vz = self.v
        from chimerax.geometry import Place
        return Place( [
            [1-2*vy*vy-2*vz*vz, 2*vx*vy-2*s*vz, 2*vx*vz+2*s*vy],
            [2*vx*vy+2*s*vz, 1-2*vx*vx-2*vz*vz, 2*vy*vz-2*s*vx],
            [2*vx*vz-2*s*vy, 2*vy*vz+2*s*vx, 1-2*vx*vx-2*vy*vy] ]
        )


    def fromMatrix ( self, rkRot ) :
        # Algorithm in Ken Shoemake's article in 1987 SIGGRAPH course notes
        # article "Quaternion Calculus and Fast Animation".

        fTrace = rkRot(0,0) + rkRot(1,1) + rkRot(2,2);
        fRoot = 0.0
        if fTrace > 0.0 :
            # |w| > 1/2, may as well choose w > 1/2
            fRoot = numpy.sqrt (fTrace + 1.0)  # 2w
            self.s = 0.5 * fRoot;
            fRoot = 0.5 / fRoot;  # 1/(4w)
            self.v[0] = (rkRot(2,1)-rkRot(1,2))*fRoot;
            self.v[1] = (rkRot(0,2)-rkRot(2,0))*fRoot;
            self.v[2] = (rkRot(1,0)-rkRot(0,1))*fRoot;

        else :
            # |w| <= 1/2
            i = 0
            if rkRot(1,1) > rkRot(0,0) : i = 1
            if rkRot(2,2) > rkRot(i,i) : i = 2

            j = i + 1 % 3  # ms_iNext[i];
            k = j + 1 % 3  # ms_iNext[j];

            fRoot = numpy.sqrt(rkRot(i,i)-rkRot(j,j)-rkRot(k,k)+1.0);

            # Real* apfQuat[3] = { &m_afTuple[1], &m_afTuple[2], &m_afTuple[3] };
            self.v[i] = 0.5 * fRoot # *apfQuat[i] = ((Real)0.5)*fRoot;

            fRoot = 0.5 / fRoot
            self.w = (rkRot(k,j)-rkRot(j,k))*fRoot
            self.v[j] = (rkRot(j,i)+rkRot(i,j))*fRoot  # *apfQuat[j]
            self.v[k] = (rkRot(k,i)+rkRot(i,k))*fRoot  # *apfQuat[k]


def mult (a, b) :
    from chimerax.geometry import cross_product
    return Quaternion (a.s*b.s - a.v*b.v, b.v*a.s + a.v*b.s + cross_product(a.v,b.v))


def slerp (p, q, t) :

    cs = p.dot(q)
    angle = numpy.arccos ( cs )

    if abs (angle) > 0.0 :
        sn = numpy.sin ( angle )
        invSn = 1.0 / sn;
        tAngle = t*angle;
        c0 = numpy.sin(angle - tAngle)*invSn;
        c1 = numpy.sin(tAngle)*invSn;

        #mTuple[0] = coeff0*p.mTuple[0] + coeff1*q.mTuple[0];
        #mTuple[1] = coeff0*p.mTuple[1] + coeff1*q.mTuple[1];
        #mTuple[2] = coeff0*p.mTuple[2] + coeff1*q.mTuple[2];
        #mTuple[3] = coeff0*p.mTuple[3] + coeff1*q.mTuple[3];
        return Quaternion (p.s*c0+q.s*c1, p.v*c0 + q.v*c1)

    else :
        return Quaternion (p.s, (p.v[0], p.v[1], p.v[2]))
