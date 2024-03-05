from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.xls.common import *
from spire.xls import *
from ctypes import *
import abc

class IPictures (  IExcelApplication) :
    """

    """
    @property
    @abc.abstractmethod
    def Count(self)->int:
        """

        """
        pass



    @abc.abstractmethod
    def get_Item(self ,Index:int)->'IPictureShape':
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,image:Image,pictureName:str)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,image:Image,pictureName:str,imageFormat:ImageFormatType)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,strFileName:str)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,strFileName:str,imageFormat:ImageFormatType)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,image:Image)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,image:Image,imageFormat:ImageFormatType)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,stream:Stream)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,stream:Stream,imageFormat:ImageFormatType)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,fileName:str)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,fileName:str,imageFormat:ImageFormatType)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,bottomRow:int,rightColumn:int,image:Image)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,bottomRow:int,rightColumn:int,image:Image,imageFormat:ImageFormatType)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,bottomRow:int,rightColumn:int,stream:Stream)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,bottomRow:int,rightColumn:int,stream:Stream,imageFormat:ImageFormatType)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,bottomRow:int,rightColumn:int,fileName:str)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,bottomRow:int,rightColumn:int,fileName:str,imageFormat:ImageFormatType)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,image:Image,scaleWidth:int,scaleHeight:int)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,image:Image,scaleWidth:int,scaleHeight:int,imageFormat:ImageFormatType)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,stream:Stream,scaleWidth:int,scaleHeight:int)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,stream:Stream,scaleWidth:int,scaleHeight:int,imageFormat:ImageFormatType)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,fileName:str,scaleWidth:int,scaleHeight:int)->IPictureShape:
        """

        """
        pass


    @dispatch

    @abc.abstractmethod
    def Add(self ,topRow:int,leftColumn:int,fileName:str,scaleWidth:int,scaleHeight:int,imageFormat:ImageFormatType)->IPictureShape:
        """

        """
        pass


