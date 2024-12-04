import {useState} from 'react'
import Image from "next/image"
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card"
import {Button} from "@/components/ui/button"
import {Input} from "@/components/ui/input"
import {Flame, Leaf, Utensils, Info, X} from 'lucide-react'

interface Product {
    name: string
    calories: number
    protein: number
    fats: number
    carbs: number
    date: string
    image: string
    weight: number
    recommends: string[]
}

interface ProductDetailProps {
    product: Product
    onClose: () => void
    onUpdate: (product: Product) => void
}

export default function ProductDetail({product, onClose, onUpdate}: ProductDetailProps) {
    const [editedProduct, setEditedProduct] = useState<Product>(product)

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target
        setEditedProduct(prev => ({
            ...prev,
            [name]: parseFloat(value) || 0
        }))
    }

    const handleUpdate = () => {
        onUpdate(editedProduct)
    }

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
            <Card className="w-full max-w-3xl max-h-[90vh] overflow-y-auto">
                <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle>{product.name}</CardTitle>
                    <Button variant="ghost" size="icon" onClick={onClose}>
                        <X className="h-6 w-6"/>
                    </Button>
                </CardHeader>
                <CardContent className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                        <div className="aspect-square relative">
                            <Image
                                src={product.image}
                                alt={product.name}
                                className="rounded-lg object-cover"
                                fill
                            />
                        </div>
                        <div className="flex flex-wrap gap-2">
                            <Button variant="outline" className="flex items-center gap-2">
                                <Flame className="h-4 w-4 text-red-500"/>
                                Мало ккал
                            </Button>
                            <Button variant="outline" className="flex items-center gap-2">
                                <Leaf className="h-4 w-4 text-green-500"/>
                                Полезно
                            </Button>
                            <Button variant="outline" className="flex items-center gap-2">
                                <Utensils className="h-4 w-4 text-purple-500"/>
                                Многоцелевой
                            </Button>
                        </div>
                    </div>
                    <div className="space-y-6">
                        <div className="space-y-2">
                            <h3 className="text-lg font-semibold flex items-center gap-2">
                                <Info className="h-5 w-5 text-blue-500"/>
                                Информация о продукте
                            </h3>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <label htmlFor="weight" className="text-sm font-medium">Вес (г)</label>
                                    <Input
                                        id="weight"
                                        name="weight"
                                        type="number"
                                        value={editedProduct.weight}
                                        onChange={handleInputChange}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label htmlFor="calories" className="text-sm font-medium">Ккал</label>
                                    <Input
                                        id="calories"
                                        name="calories"
                                        type="number"
                                        value={editedProduct.calories}
                                        onChange={handleInputChange}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label htmlFor="protein" className="text-sm font-medium">Белки (г)</label>
                                    <Input
                                        id="protein"
                                        name="protein"
                                        type="number"
                                        value={editedProduct.protein}
                                        onChange={handleInputChange}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label htmlFor="fats" className="text-sm font-medium">Жиры (г)</label>
                                    <Input
                                        id="fats"
                                        name="fats"
                                        type="number"
                                        value={editedProduct.fats}
                                        onChange={handleInputChange}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label htmlFor="carbs" className="text-sm font-medium">Углеводы (г)</label>
                                    <Input
                                        id="carbs"
                                        name="carbs"
                                        type="number"
                                        value={editedProduct.carbs}
                                        onChange={handleInputChange}
                                    />
                                </div>
                            </div>
                        </div>
                        <div className="space-y-2">
                            <h3 className="text-lg font-semibold flex items-center gap-2">
                                <Utensils className="h-5 w-5 text-orange-500"/>
                                Советы по приготовлению
                            </h3>
                            <ul className="list-disc pl-6 space-y-2">
                                {product.recommends.map((item: string, index: number) => (
                                    <li key={index}>{item.replace('.', '')}</li>
                                ))}
                            </ul>
                        </div>
                        <Button onClick={handleUpdate} className="w-full">Обновить</Button>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

